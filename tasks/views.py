from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BidForm, TaskForm
from .models import Bid, Task


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


def task_list(request):
    tasks = Task.objects.filter(status='open').order_by('deadline')
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category:
        tasks = tasks.filter(category=category)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'query': query,
        'selected_category': category,
        'categories': Task.CATEGORY_CHOICES,
    })


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    bid_form = BidForm()
    bids = task.bids.select_related('hunter').order_by('-created_at')

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'bid_form': bid_form,
        'bids': bids,
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


@login_required
def task_claim(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='open')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster == request.user:
        messages.error(request, 'You cannot claim your own bounty.')
        return redirect('task_detail', task_id=task.id)

    form = BidForm(request.POST)
    if form.is_valid():
        Bid.objects.create(
            task=task,
            hunter=request.user,
            message=form.cleaned_data['message'],
        )
        task.hunter = request.user
        task.status = 'claimed'
        task.save(update_fields=['hunter', 'status'])
        messages.success(request, 'You claimed this bounty. Contact the poster and complete it before the deadline.')

    return redirect('task_detail', task_id=task.id)
