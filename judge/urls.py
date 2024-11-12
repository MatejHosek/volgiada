from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("judge/", views.judge_view, name="judge_view"),
    path("admin/", views.admin_view, name="admin_view"),
]