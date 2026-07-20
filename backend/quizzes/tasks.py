import logging
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from django.db import models
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def _compute_streak(user):
    """Compute current and longest practice streak."""
    from .models import UserAttempt
    from django.db.models import functions

    dates = (
        UserAttempt.objects.filter(user=user, verdict="accepted")
        .annotate(date=functions.TruncDate("created_at"))
        .values_list("date", flat=True)
        .distinct()
        .order_by("-date")
    )

    if not dates:
        return 0, 0

    today = timezone.now().date()
    current = 0
    longest = 0
    streak = 0
    expected = today

    for d in dates:
        if d == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif d == expected - timedelta(days=1):
            streak += 1
            expected = d - timedelta(days=1)
        else:
            longest = max(longest, streak)
            streak = 1
            expected = d - timedelta(days=1)

    longest = max(longest, streak)

    # Check if current streak is still active (today or yesterday)
    if dates[0] == today or dates[0] == today - timedelta(days=1):
        current = streak
    else:
        current = 0

    return current, longest


def _update_user_profile(user):
    """Recalculate UserProfile stats from UserAttempt rows."""
    from .models import UserProfile

    profile, _ = UserProfile.objects.get_or_create(user=user)

    stats = user.attempts.aggregate(
        attempted=models.Count("id", distinct=True),
        solved=models.Count("id", distinct=True, filter=models.Q(verdict="accepted")),
    )

    profile.questions_attempted = stats["attempted"]
    profile.questions_solved = stats["solved"]

    current, longest = _compute_streak(user)
    profile.current_streak = current
    profile.longest_streak = max(profile.longest_streak, longest)
    profile.last_practice_date = timezone.now().date()

    profile.save()


@shared_task(time_limit=90, soft_time_limit=60)
def execute_run(code, language, test_cases):
    """Run code against public test cases. Returns results only — NO DB writes."""
    import traceback as tb_mod
    from .sandbox import execute_code

    try:
        results = []
        for tc in test_cases:
            result = execute_code(language, code, tc.get("stdin", ""))
            passed = (
                result["status"] == "success"
                and not result.get("truncated", False)
                and result["output"].strip() == tc["expected_output"].strip()
            )
            results.append({
                "passed": passed,
                "output": result["output"],
                "expected": tc["expected_output"],
                "error": result.get("error", ""),
                "status": result["status"],
                "truncated": result.get("truncated", False),
            })

        return {"results": results, "_sentinel": "ok"}

    except Exception as e:
        tb = tb_mod.format_exc()
        logger.error(f"execute_run failed: {e}\n{tb}")
        return {"results": [], "error": str(e), "traceback": tb, "_sentinel": "caught"}


@shared_task(time_limit=300, soft_time_limit=240)
def execute_submission(attempt_id, question_id, code, language):
    """Submit code against all test cases. Grades verdict. Writes to DB."""
    from .models import Question, UserAttempt
    from .sandbox import run_test_cases, QuotaExceededException, CompilerRateLimitException

    try:
        question = Question.objects.get(id=question_id)
        results = run_test_cases(question, code, language, include_hidden=True)
        all_passed = all(r["passed"] for r in results)
        verdict = "accepted" if all_passed else "wrong_answer"
        exec_time_ms = sum(int(float(r.get("time", "0")) * 1000) for r in results)

    except SoftTimeLimitExceeded:
        UserAttempt.objects.filter(id=attempt_id).update(
            verdict="runtime_error", execution_time_ms=240000)
        return {"attempt_id": attempt_id, "verdict": "runtime_error",
                "results": [], "error": "Execution timed out"}

    except QuotaExceededException:
        logger.error(f"Monthly quota exhausted — attempt {attempt_id}")
        UserAttempt.objects.filter(id=attempt_id).update(verdict="quota_exceeded")
        return {"attempt_id": attempt_id, "verdict": "quota_exceeded",
                "results": [], "error": "Monthly execution quota exceeded"}

    except CompilerRateLimitException:
        logger.warning(f"Rate limited — attempt {attempt_id}")
        UserAttempt.objects.filter(id=attempt_id).update(verdict="runtime_error")
        return {"attempt_id": attempt_id, "verdict": "runtime_error",
                "results": [], "error": "Rate limited — try again shortly"}

    except Exception as e:
        import traceback as tb_mod
        logger.error(f"execute_submission failed — attempt {attempt_id}: {e}\n{tb_mod.format_exc()}")
        UserAttempt.objects.filter(id=attempt_id).update(verdict="runtime_error")
        return {"attempt_id": attempt_id, "verdict": "runtime_error",
                "results": [], "error": str(e)}

    UserAttempt.objects.filter(id=attempt_id).update(
        verdict=verdict, execution_time_ms=exec_time_ms)
    _update_user_profile(UserAttempt.objects.get(id=attempt_id).user)
    return {"attempt_id": attempt_id, "question_id": question_id,
            "verdict": verdict, "results": results}


@shared_task
def sweep_stale_attempts():
    """Safety net for SIGKILL only. Marks stale 'skipped' attempts as runtime_error."""
    from .models import UserAttempt

    cutoff = timezone.now() - timedelta(minutes=10)
    stale = UserAttempt.objects.filter(verdict="skipped", created_at__lt=cutoff)
    count = stale.update(verdict="runtime_error")
    if count:
        logger.info(f"sweep_stale_attempts: marked {count} stale attempts as runtime_error")
    return count
