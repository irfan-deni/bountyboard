from django import forms

from .models import Task


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
