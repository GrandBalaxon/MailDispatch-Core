from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core.mixins import StyleFormMixin
from users.models import CustomUser


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Может содержать буквы, цифры и символы @ . + - _'
        self.fields['password1'].help_text = 'Пароль должен быть не менее 8 символов, не слишком простым и не состоять только из цифр.'
        self.fields['password2'].help_text = 'Введите повторно пароль для верификации.'


class CustomUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Может содержать буквы, цифры и символы @ . + - _'
