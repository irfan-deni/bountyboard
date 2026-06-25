from django import forms

from .models import Profile


# Matches the input styling used in templates/registration/register.html and login.html
INPUT_CLASSES = (
    "w-full rounded-md border border-hairline bg-surface-card "
    "px-4 py-3 text-sm text-ink focus:border-primary focus:outline-none"
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'bio', 'avatar')
        widgets = {
            'phone': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'bio': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4}),
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': (
                        "w-full rounded-md border border-hairline bg-surface-card "
                        "px-4 py-3 text-sm text-muted focus:border-primary "
                        "focus:outline-none"
                    )
                }
            ),
        }
