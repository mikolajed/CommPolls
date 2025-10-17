from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            avatar = self.cleaned_data.get('avatar')
            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(user=user)
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            avatar = self.cleaned_data.get('avatar')
            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(user=user)
            if avatar:
                profile.avatar = avatar
                profile.save()
        return user
