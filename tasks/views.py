from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Review, Task


def home(request):
    selected_category = request.GET.get('category', '').strip()
    open_tasks = Task.objects.filter(status='open').order_by('deadline')

    if selected_category:
        open_tasks = open_tasks.filter(category=selected_category)

    return render(request, 'tasks/home.html', {
        'open_tasks': open_tasks,
        'categories': Task.CATEGORY_CHOICES,
        'selected_category': selected_category,
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.poster = request.user
            task.save()
            messages.success(request, 'Your bounty is now live.')
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    reviews = task.reviews.select_related('reviewer', 'reviewee').order_by('-created_at')
    return render(request, 'tasks/task_detail.html', {'task': task, 'reviews': reviews})


@login_required
def task_claim(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='open')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster == request.user:
        messages.error(request, 'You cannot claim your own bounty.')
        return redirect('task_detail', task_id=task.id)

    task.hunter = request.user
    task.status = 'claimed'
    task.save(update_fields=['hunter', 'status'])
    messages.success(request, 'You claimed this bounty. Complete it before the deadline.')
    return redirect('task_detail', task_id=task.id)


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='claimed')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if request.user not in (task.poster, task.hunter):
        messages.error(request, 'Only the poster or hunter can mark this complete.')
        return redirect('task_detail', task_id=task.id)

    task.status = 'completed'
    task.save(update_fields=['status'])
    messages.success(request, 'Bounty marked as completed!')
    return redirect('task_detail', task_id=task.id)
