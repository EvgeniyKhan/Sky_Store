import random
import string
from urllib import request

from django.contrib.auth.hashers import make_password

from django.views.generic import CreateView, UpdateView, FormView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.http import HttpResponse

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, PasswordRecoveryForm
from users.models import User


def generate_random_password():
    length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def activate_user(request):
    key = request.GET.get('token')
    current_user = User.objects.filter(is_active=False)
    for user in current_user:
        if str(user.token) == str(key):
            user.is_active = True
            user.token = None
            user.save()
            response = redirect(reverse_lazy('users:login'))
            return response
    return HttpResponse('Неверный токен или пользователь не найден', status=400)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        secrets_token = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        new_user.token = secrets_token
        message = (f"Для подтверждения вашего профиля перейдите по ссылке http://127.0.0.1:8080/users/verifi/?token="
                   f"{secrets_token}")
        subject = 'Подтверждение регестрации'
        from_email = settings.EMAIL_HOST_USER
        recipients = [new_user.email]
        try:
            send_mail(message, subject, from_email, recipients)
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            message.error(self.request,
                          'Произошла ошибка при отправке письма. '
                          'Пожалуйста, попробуйте позже или обратитесь к администратору.')

        return super().form_valid(form)


class PasswordRecoveryView(FormView):
    template_name = 'users/recovery_password.html'
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy('users/login')

    def form_valid(self, form):
        email = form.cleaned_data.get['email']
        try:
            user = User.objects.filter(email=email).first()
        except User.DonesNotExist:
            return render(request, 'password_recovery.html',
                          {'error': 'Пользователь с таким email не найден'})
        new_password = generate_random_password()
        user.password = make_password(new_password)
        user.save()
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль {new_password}'
        from_email = settings.EMAIL_HOST_USER
        recipients = [user.email]
        send_mail(subject, message, from_email, recipients, fail_silently=False)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
