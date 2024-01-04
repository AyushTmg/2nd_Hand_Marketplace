from .utils import Util
from .models import User 
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  force_bytes
from django.contrib.auth.password_validation import validate_password

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=settings.SIGN_UP_FIELDS

class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class SendResetPasswordEmailForm(forms.Form):
    email=forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("User with the given email doesn't exist")

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = f'http://127.0.0.1:8000/reset-password/{uid}/{token}/'
        subject = "Resetting Password"
        to_email = user.email
        data = {
            "subject": subject,
            "link": link,
            "to_email": to_email
        }
        Util.send_password_reset_email(data)

        return email
    
class ResetPasswordForm(forms.Form):
    password=forms.CharField(validators=[validate_password])
    password_confirmation=forms.CharField(validators=[validate_password])

    widgets={
        'password':forms.PasswordInput,
        'password_confirmation':forms.PasswordInput,
    }

    def clean(self):
        cleaned_data=super().clean()
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Two password doesn't match")
        
        return cleaned_data

    