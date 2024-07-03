from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Profile


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        if user.email:
            send_mail(
                "Welcome to Goodreads Clone",
                f"Hi, {user.username}. Welcome to Goodreads Clone. Enjoy the books and reviews",
                "botirovmuhammadrizo61@gmail.com",
                [user.email]
            )

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']