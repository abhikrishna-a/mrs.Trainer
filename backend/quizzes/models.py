from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "roles"

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32, blank=True, default="")
    icon = models.CharField(max_length=32, blank=True, default="")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="topics")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["role", "name"]

    def __str__(self):
        return f"{self.icon} {self.name}"


class Question(models.Model):
    DIFFICULTY_CHOICES = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]
    QUESTION_TYPE_CHOICES = [("mcq", "MCQ"), ("coding", "Coding")]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=200, default="")
    slug = models.SlugField(unique=True, max_length=200)
    text = models.TextField()
    explanation = models.TextField(blank=True, default="")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default="medium")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default="mcq")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"[{self.difficulty}] {self.title or self.text[:80]}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{'*' if self.is_correct else ' '} {self.text[:50]}"


class StarterCode(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name="starter_code")
    python_code = models.TextField(blank=True, default="")
    javascript_code = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Starter code for {self.question.slug}"


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="test_cases")
    stdin = models.TextField(blank=True, default="")
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def clean(self):
        if len(self.expected_output) > 999:
            raise ValidationError("expected_output must be <= 999 chars (OnlineCompiler.io truncation limit)")

    def __str__(self):
        vis = "hidden" if self.is_hidden else "visible"
        return f"TC#{self.order} ({vis}) for {self.question.slug}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    questions_attempted = models.PositiveIntegerField(default=0)
    questions_solved = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_practice_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class UserAttempt(models.Model):
    VERDICT_CHOICES = [
        ("accepted", "Accepted"),
        ("wrong_answer", "Wrong Answer"),
        ("runtime_error", "Runtime Error"),
        ("time_limit_exceeded", "Time Limit Exceeded"),
        ("quota_exceeded", "Quota Exceeded"),
        ("skipped", "Skipped"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempts")
    selected_option = models.ForeignKey(
        AnswerOption, null=True, blank=True, on_delete=models.SET_NULL
    )
    code_submitted = models.TextField(blank=True, default="")
    language = models.CharField(max_length=20, blank=True, default="")
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, default="skipped")
    execution_time_ms = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def is_correct(self):
        return self.verdict == "accepted"

    def __str__(self):
        return f"Attempt({self.user.username}, Q#{self.question_id}, {self.verdict})"


class ExamSession(models.Model):
    MODE_CHOICES = [("full_mock", "Full Mock"), ("category_drill", "Category Drill")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_sessions")
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)

    @property
    def is_completed(self):
        return self.finished_at is not None

    @property
    def is_expired(self):
        if self.finished_at is not None:
            return False
        duration = 2700 if self.mode == "full_mock" else 1200
        return timezone.now() > self.started_at + timedelta(seconds=duration)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(finished_at__isnull=True),
                name="unique_active_session_per_user"
            )
        ]

    def __str__(self):
        return f"Exam({self.user.username}, {self.mode}, {self.get_mode_display()})"


class ExamSessionQuestion(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name="exam_questions")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        "UserAttempt", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="exam_session_questions"
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"ESQ({self.session_id}, Q#{self.question_id}, ord={self.order})"
