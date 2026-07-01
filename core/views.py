from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect, render

from tasks.models import Claim, Review, Task


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    context = {
        'total_users': User.objects.count(),
        'total_tasks': Task.objects.count(),
        'open_tasks': Task.objects.filter(status='open').count(),
        'in_progress_tasks': Task.objects.filter(status='in_progress').count(),
        'completed_tasks': Task.objects.filter(status='completed').count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
        'total_reviews': Review.objects.count(),
        'avg_rating': _safe_avg_rating(),
    }
    return render(request, 'admin/dashboard.html', context)


def _safe_avg_rating():
    avg = Review.objects.aggregate(avg=models.Avg('rating'))['avg']
    return round(avg, 1) if avg else 0
