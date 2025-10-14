from django import forms
from django.core.exceptions import ValidationError
from .models import User


def validate_password(password):
    special_chars = "!@#$%^&*()-_+="

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must include a number")
    if not any(c.isalpha() for c in password):
        raise ValidationError("Password must include a letter")
    if not any(c in special_chars for c in password):
        raise ValidationError("Password must include a special character")


class SignupForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={"placeholder": "Your email address", "class": "form-control"}
        ),
    )
    username = forms.CharField(
        max_length=45,
        widget=forms.TextInput(
            attrs={"placeholder": "Choose a username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Create a password", "class": "form-control"}
        )
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password", "class": "form-control"}
        ),
        label="Confirm Password",
    )

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)  # This will raise ValidationError
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match")


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Your email address", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Your password", "class": "form-control"}
        )
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "description", "profile_picture", "email"]
