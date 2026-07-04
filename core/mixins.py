from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.forms import BooleanField
from django.http import HttpResponseForbidden


class StyleFormMixin:
    """Миксин для автоматической стилизации полей формы Bootstrap-классами."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs.setdefault('class', '')
                field.widget.attrs['class'] += ' form-check-input'
            else:
                field.widget.attrs.setdefault('class', '')
                field.widget.attrs['class'] += ' form-control'


class UserQuerysetFilterMixin:
    """Фильтрует queryset по владельцу для обычных пользователей. Менеджеры видят все записи."""
    owner_field = 'author'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.role == 'manager':
            return qs
        if user.is_authenticated:
            return qs.filter(**{self.owner_field: user})
        return qs.none()


class OwnerOrManagerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Разрешает доступ к объекту только владельцу или менеджеру.
    Для DetailView, а также для действий, разрешённых менеджерам (например, отключение рассылки).
    """
    owner_field = 'author'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if user.role == 'manager':
            return True
        return getattr(obj, self.owner_field) == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("У вас нет прав для просмотра этого объекта.")
        return super().handle_no_permission()


class OwnerOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Только владелец объекта может выполнять действие (редактирование, удаление).
    Менеджеры не имеют права изменять чужие записи.
    """
    owner_field = 'author'

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.owner_field) == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("Только владелец может выполнять это действие.")
        return super().handle_no_permission()
