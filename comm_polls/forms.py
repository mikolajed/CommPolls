from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Poll, Choice
from django.forms import inlineformset_factory

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # avatar handled separately

    def save(self, commit=True):
        # Save user instance but don't commit yet
        user = super().save(commit=False)
        if commit:
            user.save()  # save the user first
            # Ensure profile exists
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
            user.save()  # save user first
            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(user=user)
            avatar = self.cleaned_data.get('avatar')
            if avatar is not None:
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
        required=True
    )

    class Meta:
        model = Choice
        fields = ['name']

class BaseChoiceFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        filled_forms = 0
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('name'):
                    filled_forms += 1
        
        if filled_forms < 2:
            raise forms.ValidationError('You must provide at least two choices with a name.')

# Inline formset for choices related to a poll
ChoiceFormSet = inlineformset_factory(
    Poll, 
    Choice, 
    form=ChoiceForm, 
    formset=BaseChoiceFormSet, 
    extra=0, 
    min_num=2, 
    validate_min=True, 
    can_delete=False
)