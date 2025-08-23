from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class EmailUsernameLoginForm(LoginForm):
    username = forms.CharField(label="Username", max_length=30)
    email = forms.EmailField(label="Email")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not email or not username:
            raise forms.ValidationError("Email and username are required.")

        user = authenticate(
            request=self.request,
            email=email,
            username=username,
            password=password
        )

        if user is None:
            raise forms.ValidationError("Invalid email/username/password combination.")

        self.user = user
        return cleaned_data
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label="Username")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username

    def save(self, request):
        user = super().save(request)
        return user
