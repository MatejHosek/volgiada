from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('referee/', views.refereeIndex, name='refereeIndex'),
    path('manage/', views.manageIndex, name='manageIndex'),
    path('login/', views.login, name='login')
]