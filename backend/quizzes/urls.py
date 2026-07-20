from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("auth/profile/", views.profile_view, name="profile"),

    # Content
    path("roles/", views.RoleListView.as_view(), name="role-list"),
    path("topics/", views.TopicListView.as_view(), name="topic-list"),

    # Problems
    path("problems/", views.problem_list_view, name="problem-list"),
    path("problems/<slug:slug>/", views.problem_detail_view, name="problem-detail"),
    path("problems/<slug:slug>/answer/", views.problem_answer_view, name="problem-answer"),
    path("problems/<slug:slug>/submit/", views.code_submit_view, name="problem-submit"),

    # Code execution
    path("run/", views.code_run_view, name="code-run"),
    path("tasks/<str:task_id>/", views.task_result_view, name="task-result"),

    # Exams
    path("exams/", views.exam_list_view, name="exam-list"),
    path("exams/start/", views.exam_start_view, name="exam-start"),
    path("exams/<int:pk>/", views.exam_detail_view, name="exam-detail"),
    path("exams/<int:pk>/answer/", views.exam_answer_view, name="exam-answer"),
    path("exams/<int:pk>/finish/", views.exam_finish_view, name="exam-finish"),
    path("exams/<int:pk>/results/", views.exam_results_view, name="exam-results"),
    path("exams/history/", views.exam_history_view, name="exam-history"),

    # Dashboard
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/activity/", views.activity_heatmap_view, name="dashboard-activity"),

    # Health
    path("health/", views.health_view, name="health"),

    # Config
    path("config/", views.config_view, name="config"),
]
