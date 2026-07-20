from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from .models import (
    Role, Topic, Question, AnswerOption, StarterCode, TestCase,
    UserProfile, UserAttempt, ExamSession, ExamSessionQuestion,
)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        UserProfile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "questions_attempted", "questions_solved",
                  "current_streak", "longest_streak", "last_practice_date"]


class RoleSerializer(serializers.ModelSerializer):
    topic_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "slug", "description", "topic_count"]

    def get_topic_count(self, obj):
        return obj.topics.count()


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "text", "order"]


class StarterCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarterCode
        fields = [f"{lang}_code" for lang in settings.ENABLED_LANGUAGES]


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ["id", "stdin", "expected_output", "is_hidden", "order"]


class TopicSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    difficulty_breakdown = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", "name", "short_name", "icon", "role", "order",
                  "question_count", "difficulty_breakdown"]

    def get_question_count(self, obj):
        return obj.questions.count()

    def get_difficulty_breakdown(self, obj):
        qs = obj.questions.all()
        return {
            "easy": qs.filter(difficulty="easy").count(),
            "medium": qs.filter(difficulty="medium").count(),
            "hard": qs.filter(difficulty="hard").count(),
        }


class ProblemListSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source="topic.short_name", read_only=True)
    role_name = serializers.CharField(source="topic.role.name", read_only=True)
    role_slug = serializers.CharField(source="topic.role.slug", read_only=True)
    user_solved = serializers.IntegerField(read_only=True, default=0)
    user_attempted = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Question
        fields = ["id", "title", "slug", "difficulty", "question_type",
                  "topic_name", "role_name", "role_slug",
                  "user_solved", "user_attempted"]


class ProblemDetailSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    starter_code = StarterCodeSerializer(read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)
    topic_name = serializers.CharField(source="topic.short_name", read_only=True)
    role_name = serializers.CharField(source="topic.role.name", read_only=True)

    class Meta:
        model = Question
        fields = ["id", "title", "slug", "text", "explanation", "difficulty",
                  "question_type", "topic_name", "role_name", "options",
                  "starter_code", "test_cases"]


class CodeRunSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    code = serializers.CharField()
    # Evaluated once at import — change requires server restart.
    language = serializers.ChoiceField(choices=settings.ENABLED_LANGUAGES)


class CodeSubmitSerializer(serializers.Serializer):
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=settings.ENABLED_LANGUAGES)


class ProblemAnswerSerializer(serializers.Serializer):
    selected_option_id = serializers.IntegerField()


class UserAttemptSerializer(serializers.ModelSerializer):
    is_correct = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserAttempt
        fields = ["id", "verdict", "is_correct", "execution_time_ms", "created_at"]


class ExamSessionSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = ExamSession
        fields = ["id", "mode", "role", "started_at", "finished_at",
                  "score", "total_questions", "is_completed", "is_expired"]


class ExamSessionQuestionSerializer(serializers.ModelSerializer):
    question = ProblemDetailSerializer(read_only=True)
    answer = UserAttemptSerializer(read_only=True)

    class Meta:
        model = ExamSessionQuestion
        fields = ["id", "question", "answer", "order"]


class ExamAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()


class ExamStartSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["full_mock", "category_drill"])
    role = serializers.SlugField(required=False, allow_null=True)


class DashboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["username", "questions_attempted", "questions_solved",
                  "current_streak", "longest_streak", "last_practice_date"]
