from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from tasks.models import Claim

from .forms import ProfileForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def _profile_context(request, profile_user):
    received_reviews = profile_user.received_reviews.select_related('reviewer', 'task').order_by('-created_at')
    avg_rating = profile_user.received_reviews.aggregate(avg=Avg('rating'))['avg']
    return {
        'profile_user': profile_user,
        'profile': Profile.objects.get_or_create(user=profile_user)[0],
        'is_own_profile': (
            request.user.is_authenticated and request.user == profile_user
        ),
        'posted_tasks': profile_user.posted_tasks.all().order_by('-created_at'),
        'claimed_tasks': profile_user.claimed_tasks.all().order_by('-created_at'),
        'avg_rating': avg_rating,
        'review_count': received_reviews.count(),
        'received_reviews': received_reviews,
        'pending_claims': Claim.objects.filter(hunter=profile_user, status='pending').select_related('task').order_by('-created_at'),
    }


@login_required
def profile(request):
    context = _profile_context(request, request.user)
    return render(request, 'users/profile.html', context)


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    context = _profile_context(request, profile_user)
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})
