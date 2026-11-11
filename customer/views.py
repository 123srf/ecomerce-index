from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, ContactForm
from .models import ContactInfo


from django.contrib import messages

# Create your views here.
def contact(request):
    contact_info = ContactInfo.objects.first()

    initial_data = {}
    if request.user.is_authenticated:
        initial_data['name'] = request.user.get_full_name() or request.user.username
        initial_data['email'] = request.user.email

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajınız uğurla göndərildi! Tezliklə sizinlə əlaqə saxlayacağıq.')
            return redirect('customer:contact')
        else:
            messages.error(request, 'Zəhmət olmasa formanı düzgün doldurun.')
    else:
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {
        'form': form,
        'contact_info': contact_info,
    })


def register(request):
    """Qeydiyyat: formanı yoxlayır, istifadəçi yaradır və dərhal sistemə daxil edir."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Giriş: uğurlu olduqda ana səhifəyə (və ya təhlükəsiz `next`-ə) yönləndirir."""
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
