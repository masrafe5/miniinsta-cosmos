from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class ConsumerRegistrationForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)

    class Meta:
        model  = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user       = super().save(commit=False)
        user.role  = CustomUser.ROLE_CONSUMER
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CreatorRegistrationForm(UserCreationForm):
    """Staff-only form – creates Creator accounts."""
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)

    class Meta:
        model  = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user       = super().save(commit=False)
        user.role  = CustomUser.ROLE_CREATOR
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio',
                  'profile_picture', 'website', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
