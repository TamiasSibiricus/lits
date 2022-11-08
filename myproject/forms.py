from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class UserProfileCreationForm(UserCreationForm):
    firstname = forms.CharField()
    lastname = forms.CharField()
    birth_date = forms.DateField()

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        user_profile = UserProfile(user=user)
        user_profile.firstname = self.cleaned_data.get("firstname")
        user_profile.lastname = self.cleaned_data.get("lastname")
        user_profile.birth_date = self.cleaned_data.get("birth_date")
        user_profile.save()
        user.userprofile = user_profile
        return user
