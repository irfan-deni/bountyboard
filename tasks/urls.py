from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/claim/', views.claim_task, name='claim_task'),
    path('tasks/<int:task_id>/claims/<int:claim_id>/accept/', views.accept_claim, name='accept_claim'),
    path('tasks/<int:task_id>/claims/<int:claim_id>/reject/', views.reject_claim, name='reject_claim'),
    path('tasks/<int:task_id>/proof/', views.submit_proof, name='submit_proof'),
    path('tasks/<int:task_id>/approve/', views.approve_completion, name='approve_completion'),
    path('tasks/<int:task_id>/confirm-payment/', views.confirm_payment, name='confirm_payment'),
]
