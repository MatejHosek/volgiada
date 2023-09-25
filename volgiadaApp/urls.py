from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('referee/', views.refereeIndex, name='index'),
    path('manage/', views.manageIndex, name='index'),
]