from django.contrib import admin
from django.urls import path, include

handler404 = "quizzes.views.api_not_found_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("quizzes.urls")),
]
