from django.forms import BooleanField


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
