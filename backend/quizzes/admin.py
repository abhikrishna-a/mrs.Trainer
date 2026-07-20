from django.contrib import admin
from django.contrib import messages
from .models import (
    Role, Topic, Question, AnswerOption, StarterCode, TestCase,
    UserProfile, UserAttempt, ExamSession, ExamSessionQuestion,
)


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4
    max_num = 4
    fields = ["order", "text", "is_correct"]
    ordering = ["order"]


class StarterCodeInline(admin.StackedInline):
    model = StarterCode
    extra = 0
    max_num = 1


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ["order", "stdin", "expected_output", "is_hidden"]
    ordering = ["order"]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ["title", "slug", "text", "difficulty", "question_type"]
    show_change_link = True


class ExamSessionQuestionInline(admin.TabularInline):
    model = ExamSessionQuestion
    extra = 0
    readonly_fields = ["question", "answer", "order"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "topic_count", "question_count", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}

    def topic_count(self, obj):
        return obj.topics.count()
    topic_count.short_description = "Topics"

    def question_count(self, obj):
        return Question.objects.filter(topic__role=obj).count()
    question_count.short_description = "Questions"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["icon", "name", "short_name", "role", "order", "question_count"]
    list_filter = ["role", "order"]
    search_fields = ["name", "short_name"]
    list_editable = ["order"]
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = "Questions"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "title_truncated", "topic", "difficulty", "question_type",
                    "option_count", "created_at"]
    list_filter = ["topic", "difficulty", "question_type", "topic__role"]
    search_fields = ["title", "text", "explanation"]
    list_per_page = 50
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AnswerOptionInline, StarterCodeInline, TestCaseInline]
    actions = ["make_easy", "make_medium", "make_hard", "validate_questions"]

    def title_truncated(self, obj):
        t = obj.title or obj.text[:100]
        return t[:80] + "..." if len(t) > 80 else t
    title_truncated.short_description = "Question"

    def option_count(self, obj):
        count = obj.options.count()
        correct = obj.options.filter(is_correct=True).count()
        return f"{count} ({correct} correct)"
    option_count.short_description = "Options"

    @admin.action(description="Mark selected as Easy")
    def make_easy(self, request, queryset):
        queryset.update(difficulty="easy")

    @admin.action(description="Mark selected as Medium")
    def make_medium(self, request, queryset):
        queryset.update(difficulty="medium")

    @admin.action(description="Mark selected as Hard")
    def make_hard(self, request, queryset):
        queryset.update(difficulty="hard")

    @admin.action(description="Validate question data integrity")
    def validate_questions(self, request, queryset):
        errors = []
        for q in queryset:
            if q.question_type == "mcq":
                opts = q.options.count()
                if opts < 2:
                    errors.append(f"Q#{q.id}: only {opts} options")
                elif not q.options.filter(is_correct=True).exists():
                    errors.append(f"Q#{q.id}: no correct answer")
                elif q.options.filter(is_correct=True).count() > 1:
                    errors.append(f"Q#{q.id}: multiple correct answers")
            elif q.question_type == "coding":
                if not q.test_cases.exists():
                    errors.append(f"Q#{q.id}: no test cases")
        if errors:
            self.message_user(request, f"Found {len(errors)} issues: {'; '.join(errors[:10])}", messages.WARNING)
        else:
            self.message_user(request, "All selected questions are valid.", messages.SUCCESS)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "questions_attempted", "questions_solved",
                    "current_streak", "longest_streak"]
    search_fields = ["user__username"]
    list_filter = ["current_streak"]


@admin.register(UserAttempt)
class UserAttemptAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "question_id", "verdict", "created_at"]
    list_filter = ["verdict", "language"]
    search_fields = ["user__username"]
    readonly_fields = ["user", "question", "selected_option", "code_submitted",
                       "language", "verdict", "execution_time_ms", "created_at"]
    list_per_page = 50


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "mode", "score", "total_questions",
                    "started_at", "finished_at", "is_completed"]
    list_filter = ["mode"]
    search_fields = ["user__username"]
    inlines = [ExamSessionQuestionInline]

    def is_completed(self, obj):
        return obj.is_completed
    is_completed.boolean = True
    is_completed.short_description = "Completed"
