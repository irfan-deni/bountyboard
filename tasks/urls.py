from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/claim/', views.task_claim, name='task_claim'),
    path('tasks/<int:task_id>/proof/', views.task_submit_proof, name='task_submit_proof'),
    path('tasks/<int:task_id>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:task_id>/review/', views.task_review, name='task_review'),
]
