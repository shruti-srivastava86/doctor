"""user forms"""
import re

from django import forms


class ForgotPasswordForm(forms.Form):
    """
        User forgot password form.
    """
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{8,})$')
        if not data.get('password1') == data.get('password2'):
            raise forms.ValidationError('Passwords do not match! please try again')
        if not pattern.match(data.get('password1')):
            raise forms.ValidationError('Passwords do not match')
        return data
