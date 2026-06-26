from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProofForm, TaskForm
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

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'reviews': reviews,
        'has_claimed': has_claimed,
        'claims': claims,
        'proof_form': proof_form,
        'proofs': proofs,
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
