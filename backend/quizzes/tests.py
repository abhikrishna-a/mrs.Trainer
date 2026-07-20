from django.test import TestCase, TransactionTestCase, override_settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from .models import (
    Role, Topic, Question, AnswerOption, StarterCode, TestCase as TestCaseModel,
    UserProfile, UserAttempt, ExamSession, ExamSessionQuestion,
)
from .exam_selection import borrow_with_cap, select_full_mock_questions, start_exam
from .tasks import _update_user_profile, sweep_stale_attempts


class ExamConcurrencyTest(TransactionTestCase):
    """Test that two concurrent exam_start_view calls only produce one active session."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        for i in range(10):
            q = Question.objects.create(
                topic=self.topic, title=f"Q{i}", slug=f"q-{i}", text=f"Question {i}",
                difficulty="easy", question_type="mcq", order=i,
            )
            AnswerOption.objects.create(question=q, text="A", is_correct=True, order=0)
            AnswerOption.objects.create(question=q, text="B", is_correct=False, order=1)

    def test_concurrent_exam_start_produces_one_session(self):
        from django.test import RequestFactory
        from quizzes.views import exam_start_view
        from rest_framework.test import force_authenticate

        factory = RequestFactory()
        request = factory.post("/exams/start/", {"mode": "full_mock"}, content_type="application/json")
        force_authenticate(request, user=self.user)
        response1 = exam_start_view(request)
        self.assertEqual(response1.status_code, 201)

        request2 = factory.post("/exams/start/", {"mode": "full_mock"}, content_type="application/json")
        force_authenticate(request2, user=self.user)
        response2 = exam_start_view(request2)
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(ExamSession.objects.filter(user=self.user, finished_at__isnull=True).count(), 1)


class BorrowWithCapTest(TestCase):
    """Test borrow-with-cap behavior when a role is deliberately starved."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.roles = []
        for name in ["A", "B", "C"]:
            role = Role.objects.create(name=name, slug=name.lower())
            self.roles.append(role)
            topic = Topic.objects.create(name=f"{name} Topics", short_name=name, icon="X", role=role, order=1)
            for i in range(2):
                q = Question.objects.create(
                    topic=topic, title=f"{name}-Q{i}", slug=f"{name.lower()}-q-{i}",
                    text=f"Q {name} {i}", difficulty="easy", question_type="mcq", order=i,
                )
                AnswerOption.objects.create(question=q, text="A", is_correct=True, order=0)

    def test_borrow_from_rich_role(self):
        role_a, role_b, role_c = self.roles
        result = borrow_with_cap(self.user, self.roles, needed_per_role=4, cap=2, floor=4)
        self.assertGreaterEqual(len(result[role_a]), 2)
        self.assertGreaterEqual(len(result[role_b]), 2)
        self.assertGreaterEqual(len(result[role_c]), 2)


class IsCorrectPropertyTest(TestCase):
    """Test that UserAttempt.is_correct tracks verdict correctly."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        self.question = Question.objects.create(
            topic=self.topic, title="Q1", slug="q-1", text="Test?",
            difficulty="easy", question_type="mcq", order=1,
        )
        AnswerOption.objects.create(question=self.question, text="A", is_correct=True, order=0)

    def test_is_correct_true_for_accepted(self):
        attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="accepted",
        )
        self.assertTrue(attempt.is_correct)

    def test_is_correct_false_for_wrong_answer(self):
        attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="wrong_answer",
        )
        self.assertFalse(attempt.is_correct)

    def test_is_correct_false_for_skipped(self):
        attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="skipped",
        )
        self.assertFalse(attempt.is_correct)


class ThrottleScopeTest(TestCase):
    """Test that throttle classes have correct scope attributes."""

    def test_throttle_scopes_are_set(self):
        from quizzes.views import (
            RegisterThrottle, LoginThrottle, ContentThrottle, ProfileThrottle,
            TaskResultThrottle, ExamStartThrottle, ExamDetailThrottle,
            ExamFinishThrottle, ExamResultsThrottle, ExamHistoryThrottle,
            CodeRunThrottle, CodeSubmitThrottle, CodeDailyThrottle,
            ProblemAnswerThrottle, ExamAnswerThrottle,
        )

        self.assertEqual(RegisterThrottle.scope, "register")
        self.assertEqual(LoginThrottle.scope, "login")
        self.assertEqual(ContentThrottle.scope, "content")
        self.assertEqual(ProfileThrottle.scope, "profile")
        self.assertEqual(TaskResultThrottle.scope, "task_result")
        self.assertEqual(ExamStartThrottle.scope, "exam_start")
        self.assertEqual(ExamDetailThrottle.scope, "exam_detail")
        self.assertEqual(ExamFinishThrottle.scope, "exam_finish")
        self.assertEqual(ExamResultsThrottle.scope, "exam_results")
        self.assertEqual(ExamHistoryThrottle.scope, "exam_history")
        self.assertEqual(CodeRunThrottle.scope, "code_run")
        self.assertEqual(CodeSubmitThrottle.scope, "code_submit")
        self.assertEqual(CodeDailyThrottle.scope, "code_daily")
        self.assertEqual(ProblemAnswerThrottle.scope, "problem_answer")
        self.assertEqual(ExamAnswerThrottle.scope, "exam_answer")


class SweepStaleAttemptsTest(TestCase):
    """Test that sweep_stale_attempts marks stale rows correctly."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        self.question = Question.objects.create(
            topic=self.topic, title="Q1", slug="q-1", text="Test?",
            difficulty="easy", question_type="mcq", order=1,
        )

    def test_sweep_marks_old_skipped_as_runtime_error(self):
        old = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="skipped",
        )
        old.created_at = timezone.now() - timedelta(minutes=15)
        old.save(update_fields=["created_at"])

        count = sweep_stale_attempts()
        self.assertEqual(count, 1)
        old.refresh_from_db()
        self.assertEqual(old.verdict, "runtime_error")

    def test_sweep_does_not_touch_recent_skipped(self):
        recent = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="skipped",
        )
        count = sweep_stale_attempts()
        self.assertEqual(count, 0)
        recent.refresh_from_db()
        self.assertEqual(recent.verdict, "skipped")


class FinalizeExamTest(TestCase):
    """Test that _finalize_exam sets score and finished_at."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        self.question = Question.objects.create(
            topic=self.topic, title="Q1", slug="q-1", text="Test?",
            difficulty="easy", question_type="mcq", order=1,
        )
        AnswerOption.objects.create(question=self.question, text="A", is_correct=True, order=0)

    def test_finalize_exam_sets_score_and_finished_at(self):
        from quizzes.views import _finalize_exam

        session = ExamSession.objects.create(user=self.user, mode="full_mock", total_questions=1)
        attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="accepted",
        )
        ExamSessionQuestion.objects.create(session=session, question=self.question, answer=attempt, order=0)

        _finalize_exam(session)

        session.refresh_from_db()
        self.assertEqual(session.score, 1)
        self.assertIsNotNone(session.finished_at)
        self.assertTrue(session.is_completed)

    def test_finalize_exam_with_wrong_answer(self):
        from quizzes.views import _finalize_exam

        session = ExamSession.objects.create(user=self.user, mode="full_mock", total_questions=1)
        attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="wrong_answer",
        )
        ExamSessionQuestion.objects.create(session=session, question=self.question, answer=attempt, order=0)

        _finalize_exam(session)

        session.refresh_from_db()
        self.assertEqual(session.score, 0)


class ExecuteSubmissionExceptionTest(TestCase):
    """Test that execute_submission handles broad exceptions."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        self.question = Question.objects.create(
            topic=self.topic, title="Q1", slug="q-1", text="Test?",
            difficulty="easy", question_type="mcq", order=1,
        )
        self.attempt = UserAttempt.objects.create(
            user=self.user, question=self.question, verdict="skipped",
        )

    @patch("quizzes.sandbox.run_test_cases")
    def test_quota_exceeded_sets_quota_exceeded(self, mock_run):
        from quizzes.sandbox import QuotaExceededException
        from quizzes.tasks import execute_submission

        mock_run.side_effect = QuotaExceededException("quota exceeded")
        result = execute_submission(self.attempt.id, self.question.id, "code", "python")

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.verdict, "quota_exceeded")
        self.assertEqual(result["verdict"], "quota_exceeded")

    @patch("quizzes.sandbox.run_test_cases")
    def test_generic_exception_sets_runtime_error(self, mock_run):
        from quizzes.tasks import execute_submission

        mock_run.side_effect = RuntimeError("something broke")
        result = execute_submission(self.attempt.id, self.question.id, "code", "python")

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.verdict, "runtime_error")

    @patch("quizzes.sandbox.run_test_cases")
    def test_question_not_found_sets_runtime_error(self, mock_run):
        from quizzes.tasks import execute_submission

        result = execute_submission(self.attempt.id, 99999, "code", "python")

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.verdict, "runtime_error")


class ExamSessionIsCompletedTest(TestCase):
    """Test that ExamSession.is_completed derives from finished_at."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_is_completed_false_when_no_finished_at(self):
        session = ExamSession.objects.create(user=self.user, mode="full_mock")
        self.assertFalse(session.is_completed)

    def test_is_completed_true_when_finished_at_set(self):
        session = ExamSession.objects.create(user=self.user, mode="full_mock")
        session.finished_at = timezone.now()
        session.save(update_fields=["finished_at"])
        self.assertTrue(session.is_completed)


class UniqueActiveSessionConstraintTest(TransactionTestCase):
    """Test that the UniqueConstraint prevents two active sessions."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_cannot_create_two_active_sessions(self):
        ExamSession.objects.create(user=self.user, mode="full_mock")
        with self.assertRaises(IntegrityError):
            ExamSession.objects.create(user=self.user, mode="full_mock")

    def test_can_create_new_session_after_finishing(self):
        s1 = ExamSession.objects.create(user=self.user, mode="full_mock")
        s1.finished_at = timezone.now()
        s1.save(update_fields=["finished_at"])

        s2 = ExamSession.objects.create(user=self.user, mode="full_mock")
        self.assertIsNotNone(s2.id)


class UserProfileUpdateTest(TestCase):
    """Test that _update_user_profile recalculates stats from UserAttempt."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.role = Role.objects.create(name="Python", slug="python")
        self.topic = Topic.objects.create(name="Basics", short_name="BAS", icon="P", role=self.role, order=1)
        self.question = Question.objects.create(
            topic=self.topic, title="Q1", slug="q-1", text="Test?",
            difficulty="easy", question_type="mcq", order=1,
        )

    def test_profile_updates_after_mcq_answer(self):
        UserAttempt.objects.create(user=self.user, question=self.question, verdict="accepted")
        _update_user_profile(self.user)

        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.questions_solved, 1)

    def test_profile_updates_after_multiple_attempts(self):
        for i in range(3):
            q = Question.objects.create(
                topic=self.topic, title=f"MultiQ{i}", slug=f"multi-q-{i}", text=f"Q{i}",
                difficulty="easy", question_type="mcq", order=i + 10,
            )
            verdict = "accepted" if i < 2 else "wrong_answer"
            UserAttempt.objects.create(user=self.user, question=q, verdict=verdict)

        _update_user_profile(self.user)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.questions_attempted, 3)
        self.assertEqual(self.user.profile.questions_solved, 2)


class Api404Test(TestCase):
    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_unmatched_api_path_returns_json(self):
        response = self.client.get("/api/tasks//")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "error": True, "status_code": 404, "detail": "Not found."
        })

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
    def test_unmatched_non_api_path_uses_default_404(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response["Content-Type"], "application/json")


class TaskResultViewTest(TestCase):
    def test_failed_task_returns_json_not_500(self):
        from unittest.mock import patch, MagicMock
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework.test import APIClient

        user = User.objects.create_user(username="t3", password="pass1234")
        client = APIClient()
        token = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

        with patch("celery.result.AsyncResult") as MockResult:
            mock_result = MagicMock()
            mock_result.status = "FAILURE"
            mock_result.ready.return_value = True
            mock_result.result = RuntimeError("something broke")
            MockResult.return_value = mock_result

            response = client.get("/api/tasks/fake-uuid/")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "FAILURE"
            assert data["result"]["error"] == "something broke"
