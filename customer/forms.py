from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage


class BootstrapFormMixin:
    """Bütün sahələrə Bootstrap siniflərini əlavə edir və uzun help_text mətnlərini gizlədir."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css_class = widget.attrs.get('class', '')
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = f'{css_class} form-check-input'.strip()
            else:
                widget.attrs['class'] = f'{css_class} form-control'.strip()
            if not isinstance(widget, (forms.CheckboxInput, forms.HiddenInput)):
                widget.attrs.setdefault('placeholder', field.label)
            # Uzun izahat siyahıları gizlədilir; qaydalar pozulduqda xəta kimi görünür.
            field.help_text = None


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    """Qeydiyyat formu: istifadəçi adı, e-poçt, parol, parolun təkrarı."""

    email = forms.EmailField(label=_('Email'), required=True)

    field_order = ['username', 'email', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('A user with this email already exists.'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Giriş formu (xəta mesajları Django tərəfindən idarə olunur)."""

    pass


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    """Əlaqə formu: ad, e-poçt, mövzu, mesaj."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Your Name'), 'id': 'name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': _('Your Email'), 'id': 'email', 'required': 'required'}),
            'subject': forms.TextInput(attrs={'placeholder': _('Subject'), 'id': 'subject', 'required': 'required'}),
            'message': forms.Textarea(attrs={'placeholder': _('Message'), 'id': 'message', 'rows': 8, 'required': 'required'}),
        }

