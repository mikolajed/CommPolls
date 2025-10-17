from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

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
