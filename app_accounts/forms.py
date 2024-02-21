from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from app_accounts.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password1', 'password2')


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('full_name', 'comment')


class UserBlockUnblockForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('full_name', 'email', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True


class UserResetPasswordForm(forms.Form):
    user_email = forms.EmailField()
    captcha = CaptchaField()

    def clean_user_email(self):
        # TODO: if captcha invalid raise exception
        email = self.cleaned_data.get('user_email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователя с таким email не найдено!')
        return email
