import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import (
    Role, Topic, Question, AnswerOption, StarterCode,
    UserProfile, UserAttempt, ExamSession, ExamSessionQuestion,
)
from .serializers import (
    RegisterSerializer, ProfileSerializer, RoleSerializer, TopicSerializer,
    ProblemListSerializer, ProblemDetailSerializer,
    CodeRunSerializer, CodeSubmitSerializer, ProblemAnswerSerializer,
    ExamSessionSerializer, ExamSessionQuestionSerializer,
    ExamAnswerSerializer, ExamStartSerializer, DashboardSerializer,
)
from .exam_selection import start_exam
from .tasks import execute_run, execute_submission, _update_user_profile

logger = logging.getLogger(__name__)


# ─── Throttle Classes ──────────────────────────────────

class RegisterThrottle(UserRateThrottle):
    scope = "register"

class LoginThrottle(UserRateThrottle):
    scope = "login"

class ContentThrottle(UserRateThrottle):
    scope = "content"

class ProfileThrottle(UserRateThrottle):
    scope = "profile"

class TaskResultThrottle(UserRateThrottle):
    scope = "task_result"

class ExamStartThrottle(UserRateThrottle):
    scope = "exam_start"

class ExamDetailThrottle(UserRateThrottle):
    scope = "exam_detail"

class ExamFinishThrottle(UserRateThrottle):
    scope = "exam_finish"

class ExamResultsThrottle(UserRateThrottle):
    scope = "exam_results"

class ExamHistoryThrottle(UserRateThrottle):
    scope = "exam_history"

class CodeRunThrottle(UserRateThrottle):
    scope = "code_run"

class CodeSubmitThrottle(UserRateThrottle):
    scope = "code_submit"

class CodeDailyThrottle(UserRateThrottle):
    scope = "code_daily"

class ProblemAnswerThrottle(UserRateThrottle):
    scope = "problem_answer"

class ExamAnswerThrottle(UserRateThrottle):
    scope = "exam_answer"


# ─── Auth ──────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [RegisterThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": {"id": user.id, "username": user.username, "email": user.email},
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(response.data["access"])
            user_id = access_token["user_id"]
            try:
                user = User.objects.get(id=user_id)
                response.data = {
                    "user": {
                        "id": user.id, "username": user.username, "email": user.email,
                    },
                    "tokens": {
                        "access": response.data["access"],
                        "refresh": response.data["refresh"],
                    },
                }
            except User.DoesNotExist:
                pass
        return response


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass
    return Response({"detail": "Logged out."}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([ProfileThrottle])
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


# ─── Content ───────────────────────────────────────────

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContentThrottle]


class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContentThrottle]

    def get_queryset(self):
        role_slug = self.request.query_params.get("role")
        qs = Topic.objects.all()
        if role_slug:
            qs = qs.filter(role__slug=role_slug)
        return qs


# ─── Problems ──────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([ContentThrottle])
def problem_list_view(request):
    qs = Question.objects.select_related("topic", "topic__role").all()

    role = request.query_params.get("role")
    if role:
        qs = qs.filter(topic__role__slug=role)

    topic = request.query_params.get("topic")
    if topic:
        qs = qs.filter(topic__short_name__iexact=topic)

    difficulty = request.query_params.get("difficulty")
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    qtype = request.query_params.get("type")
    if qtype:
        qs = qs.filter(question_type=qtype)

    if request.user.is_authenticated:
        solved_ids = UserAttempt.objects.filter(
            user=request.user, verdict="accepted"
        ).values_list("question_id", flat=True)
        qs = qs.annotate(
            user_solved=Count("id", filter=Q(id__in=solved_ids)),
            user_attempted=Count("id", filter=Q(attempts__user=request.user)),
        )

    serializer = ProblemListSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([ContentThrottle])
def problem_detail_view(request, slug):
    question = get_object_or_404(
        Question.objects.select_related("topic", "topic__role"),
        slug=slug,
    )
    serializer = ProblemDetailSerializer(question)
    data = serializer.data

    if request.user.is_authenticated:
        attempt = UserAttempt.objects.filter(
            user=request.user, question=question
        ).order_by("-created_at").first()
        if attempt:
            data["user_status"] = "solved" if attempt.verdict == "accepted" else "attempted"
        else:
            data["user_status"] = "unattempted"

    return Response(data)


# ─── Code Run ──────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([CodeRunThrottle])
def code_run_view(request):
    serializer = CodeRunSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    question = get_object_or_404(Question, slug=serializer.validated_data["slug"])
    code = serializer.validated_data["code"]
    language = serializer.validated_data["language"]

    test_cases = list(
        question.test_cases.filter(is_hidden=False)
        .values("stdin", "expected_output")
    )

    task = execute_run.delay(code, language, test_cases)
    return Response({"task_id": str(task.id)}, status=202)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([CodeSubmitThrottle, CodeDailyThrottle])
def code_submit_view(request, **kwargs):
    serializer = CodeSubmitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    question = get_object_or_404(Question, slug=kwargs["slug"])
    code = serializer.validated_data["code"]
    language = serializer.validated_data["language"]

    attempt = UserAttempt.objects.create(
        user=request.user,
        question=question,
        code_submitted=code,
        language=language,
        verdict="skipped",
    )

    task = execute_submission.delay(attempt.id, question.id, code, language)
    return Response(
        {"task_id": str(task.id), "attempt_id": attempt.id},
        status=202,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([TaskResultThrottle])
def task_result_view(request, task_id):
    from celery.result import AsyncResult

    result = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "status": result.status,
        "result": None,
    }

    if result.ready():
        if isinstance(result.result, Exception):
            response["result"] = {"error": str(result.result)}
        else:
            response["result"] = result.result

    return Response(response)


# ─── MCQ Practice Answer ───────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ProblemAnswerThrottle])
def problem_answer_view(request, slug):
    question = get_object_or_404(Question, slug=slug, question_type="mcq")
    serializer = ProblemAnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    selected_option_id = serializer.validated_data["selected_option_id"]
    correct_option = AnswerOption.objects.filter(question=question, is_correct=True).first()
    verdict = "accepted" if (correct_option and correct_option.id == selected_option_id) else "wrong_answer"

    attempt = UserAttempt.objects.create(
        user=request.user,
        question=question,
        selected_option_id=selected_option_id,
        verdict=verdict,
    )
    _update_user_profile(request.user)
    return Response({
        "is_correct": attempt.is_correct,
        "explanation": question.explanation,
        "correct_option_id": correct_option.id if correct_option else None,
    })


# ─── Exams ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamHistoryThrottle])
def exam_list_view(request):
    sessions = ExamSession.objects.filter(user=request.user).order_by("-started_at")[:50]
    serializer = ExamSessionSerializer(sessions, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamStartThrottle])
def exam_start_view(request):
    serializer = ExamStartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mode = serializer.validated_data["mode"]
    role_slug = serializer.validated_data.get("role")
    role = None
    if role_slug:
        role = get_object_or_404(Role, slug=role_slug)

    try:
        session = start_exam(request.user, mode, role)
    except IntegrityError:
        existing = ExamSession.objects.filter(
            user=request.user, finished_at__isnull=True
        ).first()
        if existing:
            return Response(ExamSessionSerializer(existing).data, status=200)
        return Response(
            {"detail": "Failed to create exam session."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(ExamSessionSerializer(session).data, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamDetailThrottle])
def exam_detail_view(request, pk):
    session = get_object_or_404(ExamSession, pk=pk, user=request.user)
    if session.is_expired and not session.is_completed:
        _finalize_exam(session)

    esqs = session.exam_questions.select_related("question", "question__topic").all()
    return Response({
        "session": ExamSessionSerializer(session).data,
        "questions": ExamSessionQuestionSerializer(esqs, many=True).data,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamAnswerThrottle])
def exam_answer_view(request, pk):
    session = get_object_or_404(ExamSession, pk=pk, user=request.user)

    if session.is_completed:
        return Response({"detail": "Exam already completed."}, status=400)
    if session.is_expired:
        _finalize_exam(session)
        return Response({"detail": "Time expired."}, status=400)

    serializer = ExamAnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    question_id = serializer.validated_data["question_id"]
    selected_option_id = serializer.validated_data["selected_option_id"]

    esq = get_object_or_404(ExamSessionQuestion, session=session, question_id=question_id)
    correct_option = AnswerOption.objects.filter(
        question_id=question_id, is_correct=True
    ).first()
    verdict = "accepted" if (correct_option and correct_option.id == selected_option_id) else "wrong_answer"

    attempt = UserAttempt.objects.create(
        user=request.user,
        question_id=question_id,
        selected_option_id=selected_option_id,
        verdict=verdict,
    )
    esq.answer = attempt
    esq.save(update_fields=["answer"])
    _update_user_profile(request.user)

    return Response({"is_correct": attempt.is_correct})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamFinishThrottle])
def exam_finish_view(request, pk):
    session = get_object_or_404(ExamSession, pk=pk, user=request.user)
    if session.is_completed:
        return Response(ExamSessionSerializer(session).data)

    _finalize_exam(session)
    return Response(ExamSessionSerializer(session).data)


def _finalize_exam(session):
    """Compute score and mark exam complete. Single source of truth."""
    correct = ExamSessionQuestion.objects.filter(
        session=session, answer__verdict="accepted"
    ).count()
    session.score = correct
    session.finished_at = timezone.now()
    session.save(update_fields=["score", "finished_at"])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamResultsThrottle])
def exam_results_view(request, pk):
    session = get_object_or_404(ExamSession, pk=pk, user=request.user)
    if not session.is_completed:
        return Response({"detail": "Exam not completed."}, status=400)

    esqs = session.exam_questions.select_related("question").all()
    results = []
    for esq in esqs:
        answer = esq.answer
        correct_option = AnswerOption.objects.filter(
            question=esq.question, is_correct=True
        ).first()
        results.append({
            "question_id": esq.question_id,
            "question_text": esq.question.text,
            "selected_option_id": answer.selected_option_id if answer else None,
            "correct_option_id": correct_option.id if correct_option else None,
            "is_correct": answer.verdict == "accepted" if answer else False,
            "explanation": esq.question.explanation,
        })

    return Response({
        "session": ExamSessionSerializer(session).data,
        "results": results,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@throttle_classes([ExamHistoryThrottle])
def exam_history_view(request):
    sessions = ExamSession.objects.filter(
        user=request.user, finished_at__isnull=False
    ).order_by("-finished_at")[:50]
    return Response(ExamSessionSerializer(sessions, many=True).data)


# ─── Dashboard ─────────────────────────────────────────

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    _update_user_profile(request.user)
    profile.refresh_from_db()
    return Response(DashboardSerializer(profile).data)


# ─── Health ────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
def health_view(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False

    return Response({"status": "ok" if db_ok else "degraded", "db": db_ok})


# ─── 404 Handler ───────────────────────────────────────

from django.http import JsonResponse
from django.views.defaults import page_not_found


def api_not_found_view(request, exception):
    if request.path.startswith("/api/"):
        return JsonResponse(
            {"error": True, "status_code": 404, "detail": "Not found."},
            status=404,
        )
    return page_not_found(request, exception)


# ─── Config ─────────────────────────────────────────────

@api_view(["GET"])
@permission_classes([AllowAny])
@throttle_classes([ContentThrottle])
def config_view(request):
    return Response({"enabled_languages": settings.ENABLED_LANGUAGES})
