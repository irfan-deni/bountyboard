from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProofForm, ReviewForm, TaskForm
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
    proof_form = ProofForm(instance=task)
    review_form = ReviewForm()
    can_review = (
        request.user.is_authenticated
        and task.status == 'completed'
        and request.user in (task.poster, task.hunter)
        and task.hunter is not None
        and not reviews.filter(reviewer=request.user).exists()
    )

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'proof_form': proof_form,
        'review_form': review_form,
        'reviews': reviews,
        'can_review': can_review,
    })


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
def task_submit_proof(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='claimed', hunter=request.user)

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    form = ProofForm(request.POST, request.FILES, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proof submitted. The task creator can now approve completion.')
    else:
        messages.error(request, 'Please check your proof submission and try again.')

    return redirect('task_detail', task_id=task.id)


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='claimed')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if request.user != task.poster:
        messages.error(request, 'Only the task creator can approve completion.')
        return redirect('task_detail', task_id=task.id)

    task.status = 'completed'
    task.save(update_fields=['status'])
    messages.success(request, 'Bounty marked as completed!')
    return redirect('task_detail', task_id=task.id)


@login_required
def task_review(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='completed')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.hunter is None or request.user not in (task.poster, task.hunter):
        messages.error(request, 'Only task participants can leave a review.')
        return redirect('task_detail', task_id=task.id)

    if Review.objects.filter(task=task, reviewer=request.user).exists():
        messages.error(request, 'You already reviewed this bounty.')
        return redirect('task_detail', task_id=task.id)

    reviewee = task.hunter if request.user == task.poster else task.poster
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.task = task
        review.reviewer = request.user
        review.reviewee = reviewee
        review.save()
        messages.success(request, 'Review submitted.')
    else:
        messages.error(request, 'Please check your review and try again.')

    return redirect('task_detail', task_id=task.id)
