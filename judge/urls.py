from django.urls import path

from . import views

app_name = "judge"
urlpatterns = [
    path("", views.index, name="index"),
    path("judge/", views.judge_view, name="judge_view"),
    path("admin/", views.admin_view, name="admin_view"),
    path("login/<str:redirect_view>/", views.login_view, name="login_view")
]