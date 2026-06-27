from django import forms

from .models import Proof, Task, Review


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'bounty', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
                'placeholder': 'Print and deliver my assignment',
            }),
            'description': forms.Textarea(attrs={
                'class': 'min-h-32 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
                'placeholder': 'Describe the task, location, and any special instructions.',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
            }),
            'bounty': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
                'min': '1',
                'step': '0.50',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
                'type': 'datetime-local',
            }),
        }


class ProofForm(forms.ModelForm):
    class Meta:
        model = Proof
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
            }),
            'description': forms.Textarea(attrs={
                'class': 'min-h-24 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm focus:border-brand focus:outline-none focus:ring-2 focus:ring-indigo-100',
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
                'class': 'w-full rounded-md border border-hairline bg-surface-card px-4 py-3 text-sm text-ink focus:border-primary focus:outline-none',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full rounded-md border border-hairline bg-surface-card px-4 py-3 text-sm text-ink focus:border-primary focus:outline-none',
                'rows': 3,
                'placeholder': 'Share how it went...',
            }),
        }
