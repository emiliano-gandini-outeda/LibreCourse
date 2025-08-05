from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    username = forms.CharField(
        max_length=150, 
        required=True,
        error_messages={
            'unique': "This username is already taken.",
            'required': "Please enter a username.",
        }
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'unique': "Email already registered.",
            'invalid': "Enter a valid email address.",
            'required': "Email is required.",
        }
    )

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data["username"]
        user.save()
        return user