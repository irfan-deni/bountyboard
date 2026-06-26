from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    CATEGORY_CHOICES = [
        ('delivery', 'Delivery'),
        ('coding', 'Coding Help'),
        ('design', 'Design'),
        ('tutoring', 'Tutoring'),
        ('errands', 'Errands'),
        ('photography', 'Photography'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ]

    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_tasks')
    hunter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    bounty = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='open')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - RM{self.bounty}"


class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='claims')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'hunter')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.hunter.username} → {self.task.title} ({self.status})"


class Proof(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='proofs')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='proofs/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proof for {self.task.title} by {self.hunter.username}"


class Review(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} → {self.reviewee.username}"
