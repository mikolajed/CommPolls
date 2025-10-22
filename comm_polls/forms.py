from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Poll, Choice
from django.forms import inlineformset_factory

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # Remove default help text
        for field in self.fields.values():
            if field.required and field.label:
                field.label = f"{field.label}*"

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # avatar handled separately

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']  # avatar handled separately

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Favorite Programming Language?'}),
            'description': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Optional: Add more context to your poll...'}
            ),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ChoiceForm(forms.ModelForm):
    name = forms.CharField(
        label='Choice Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter choice name'}),
        required=False  # Validation handled in formset
    )

    class Meta:
        model = Choice
        fields = ['name']


class BaseChoiceFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        # Count only forms that have a non-empty 'name' field and are not deleted
        filled_forms = 0
        for form in self.forms:
            if hasattr(form, 'cleaned_data'):
                name = form.cleaned_data.get('name', '').strip()
                delete = form.cleaned_data.get('DELETE', False)
                if name and not delete:
                    filled_forms += 1

        if filled_forms < 2:
            raise forms.ValidationError(
                'You must provide at least two choices with a name.'
            )


# Inline formset for choices related to a poll
ChoiceFormSet = inlineformset_factory(
    Poll,
    Choice,
    form=ChoiceForm,
    formset=BaseChoiceFormSet,
    extra=0,
    min_num=2,
    validate_min=False,  # Custom clean handles validation
    can_delete=False
)
