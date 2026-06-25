from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/claim/', views.task_claim, name='task_claim'),
    path('tasks/<int:task_id>/complete/', views.task_complete, name='task_complete'),
]
