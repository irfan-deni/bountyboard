from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    posted_tasks = request.user.posted_tasks.order_by('-created_at')
    claimed_tasks = request.user.claimed_tasks.order_by('-created_at')
    reviews = request.user.received_reviews.select_related('reviewer', 'task').order_by('-created_at')

    return render(request, 'users/profile.html', {
        'posted_tasks': posted_tasks,
        'claimed_tasks': claimed_tasks,
        'reviews': reviews,
    })
