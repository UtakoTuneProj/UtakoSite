from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.views import generic

from .forms import LoginForm, ResetPasswordForm

class Login(LoginView):
    form_class = LoginForm
    template_name = 'register/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'register/logout.html'

class PasswordReset(PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'register/password_reset.html'
    email_template_name = 'register/password_reset_email.html'
    email_template_name = 'register/password_reset_subject.html'
    success_url = '/auth/password_reset/done'

class PasswordResetDone(PasswordResetDoneView):
    form_class = ResetPasswordForm
    template_name = 'register/password_reset_done.html'
