from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from .forms import ProofForm, TaskForm, ReviewForm
from .models import Claim, Proof, Review, Task


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

    has_claimed = False
    claims = []
    proof_form = None
    proofs = []

    if request.user.is_authenticated:
        if task.status == 'open' and task.poster != request.user:
            has_claimed = Claim.objects.filter(task=task, hunter=request.user).exists()

        if task.poster == request.user:
            claims = task.claims.filter(status='pending').select_related('hunter__profile')

        if task.status == 'in_progress' and task.hunter == request.user:
            proof_form = ProofForm()
            proofs = task.proofs.all()

        if task.poster == request.user:
            proofs = task.proofs.select_related('hunter').all()

    my_review = None
    can_review = False
    if (request.user.is_authenticated and task.status in ('completed', 'done')
            and task.hunter is not None and request.user in (task.poster, task.hunter)):
        my_review = Review.objects.filter(task=task, reviewer=request.user).first()
        can_review = my_review is None
    review_form = ReviewForm() if can_review else None

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'reviews': reviews,
        'has_claimed': has_claimed,
        'claims': claims,
        'proof_form': proof_form,
        'proofs': proofs,
        'review_form': review_form,
        'can_review': can_review,
        'my_review': my_review,
    })


@login_required
def claim_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='open')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster == request.user:
        messages.error(request, 'You cannot claim your own bounty.')
        return redirect('task_detail', task_id=task.id)

    _, created = Claim.objects.get_or_create(task=task, hunter=request.user)
    if created:
        messages.success(request, 'Your claim has been submitted. The poster will review it.')
    else:
        messages.info(request, 'You already claimed this bounty.')

    return redirect('task_detail', task_id=task.id)


@login_required
def accept_claim(request, task_id, claim_id):
    task = get_object_or_404(Task, id=task_id, status='open')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster != request.user:
        messages.error(request, 'Only the poster can accept claims.')
        return redirect('task_detail', task_id=task.id)

    claim = get_object_or_404(Claim, id=claim_id, task=task, status='pending')

    claim.status = 'accepted'
    claim.save(update_fields=['status'])

    task.hunter = claim.hunter
    task.status = 'in_progress'
    task.save(update_fields=['hunter', 'status'])

    Claim.objects.filter(task=task, status='pending').exclude(id=claim.id).update(status='rejected')

    messages.success(request, f'Accepted {claim.hunter.username} for this bounty.')
    return redirect('task_detail', task_id=task.id)


@login_required
def reject_claim(request, task_id, claim_id):
    task = get_object_or_404(Task, id=task_id, status='open')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster != request.user:
        messages.error(request, 'Only the poster can reject claims.')
        return redirect('task_detail', task_id=task.id)

    claim = get_object_or_404(Claim, id=claim_id, task=task, status='pending')
    claim.status = 'rejected'
    claim.save(update_fields=['status'])

    messages.success(request, f'Rejected {claim.hunter.username}.')
    return redirect('task_detail', task_id=task.id)


@login_required
def submit_proof(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='in_progress')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.hunter != request.user:
        messages.error(request, 'Only the assigned hunter can submit proof.')
        return redirect('task_detail', task_id=task.id)

    form = ProofForm(request.POST, request.FILES)
    if form.is_valid():
        proof = form.save(commit=False)
        proof.task = task
        proof.hunter = request.user
        proof.save()
        messages.success(request, 'Proof submitted! Waiting for the poster to approve.')
    else:
        for error in form.errors.values():
            messages.error(request, error)

    return redirect('task_detail', task_id=task.id)


@login_required
def approve_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='in_progress')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.poster != request.user:
        messages.error(request, 'Only the poster can approve completion.')
        return redirect('task_detail', task_id=task.id)

    task.status = 'completed'
    task.save(update_fields=['status'])
    messages.success(request, 'Bounty marked as completed! Waiting for the hunter to confirm payment.')
    return redirect('task_detail', task_id=task.id)


@login_required
def confirm_payment(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='completed')

    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)

    if task.hunter != request.user:
        messages.error(request, 'Only the assigned hunter can confirm payment.')
        return redirect('task_detail', task_id=task.id)

    task.status = 'done'
    task.save(update_fields=['status'])
    messages.success(request, 'Payment confirmed! Bounty complete.')
    return redirect('task_detail', task_id=task.id)


@login_required
def review_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method != 'POST':
        return redirect('task_detail', task_id=task.id)
    if task.status not in ('completed', 'done'):
        messages.error(request, 'You can only review a completed bounty.')
        return redirect('task_detail', task_id=task.id)
    if task.hunter is None or request.user not in (task.poster, task.hunter):
        messages.error(request, 'Only the poster or hunter can leave a review.')
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
        messages.success(request, 'Review submitted. Thanks for the feedback!')
    else:
        messages.error(request, 'Please provide a valid rating and comment.')
    return redirect('task_detail', task_id=task.id)


def browse(request):
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    min_bounty = request.GET.get('min_bounty', '').strip()
    max_bounty = request.GET.get('max_bounty', '').strip()
    deadline_before = request.GET.get('deadline_before', '').strip()

    tasks = Task.objects.filter(status='open').order_by('deadline')
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if selected_category:
        tasks = tasks.filter(category=selected_category)
    if min_bounty:
        try:
            tasks = tasks.filter(bounty__gte=Decimal(min_bounty))
        except (InvalidOperation, ValueError):
            pass
    if max_bounty:
        try:
            tasks = tasks.filter(bounty__lte=Decimal(max_bounty))
        except (InvalidOperation, ValueError):
            pass
    if deadline_before:
        parsed = parse_date(deadline_before)
        if parsed:
            tasks = tasks.filter(deadline__date__lte=parsed)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'categories': Task.CATEGORY_CHOICES,
        'selected_category': selected_category,
        'query': query,
        'min_bounty': min_bounty,
        'max_bounty': max_bounty,
        'deadline_before': deadline_before,
    })


@login_required
def my_tasks(request):
    posted_tasks = request.user.posted_tasks.all().order_by('-created_at')
    assigned_tasks = request.user.claimed_tasks.all().order_by('-created_at')
    pending_claims = Claim.objects.filter(hunter=request.user, status='pending').select_related('task').order_by('-created_at')
    return render(request, 'tasks/my_tasks.html', {
        'posted_tasks': posted_tasks,
        'assigned_tasks': assigned_tasks,
        'pending_claims': pending_claims,
    })
