from django.shortcuts import render

from .models import Task


def home(request):
    open_tasks = Task.objects.filter(status='open').order_by('-created_at')[:6]
    return render(request, 'tasks/home.html', {'open_tasks': open_tasks})
