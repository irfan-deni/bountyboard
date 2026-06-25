from django import forms

from .models import Review, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'bounty', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'pixel-input',
                'placeholder': 'Print and deliver my assignment',
            }),
            'description': forms.Textarea(attrs={
                'class': 'pixel-input min-h-32',
                'placeholder': 'Describe the task, location, and any special instructions.',
            }),
            'category': forms.Select(attrs={
                'class': 'pixel-input',
            }),
            'bounty': forms.NumberInput(attrs={
                'class': 'pixel-input',
                'min': '1',
                'step': '0.50',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'pixel-input',
                'type': 'datetime-local',
            }),
        }


class ProofForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['proof_note', 'proof_image']
        widgets = {
            'proof_note': forms.Textarea(attrs={
                'class': 'pixel-input min-h-28',
                'placeholder': 'Describe what you completed, where you delivered it, or any handover details.',
            }),
            'proof_image': forms.ClearableFileInput(attrs={
                'class': 'pixel-input',
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'pixel-input',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'pixel-input min-h-28',
                'placeholder': 'Share a short, honest review.',
            }),
        }
