from django import forms

from .models import Proof, Task, Review


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
                'class': 'pixel-input',
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
        model = Proof
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'pixel-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'pixel-input',
                'placeholder': 'Optional description of the completed work.',
                'rows': 3,
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
                'class': 'pixel-input',
                'rows': 3,
                'placeholder': 'Share how it went...',
            }),
        }
