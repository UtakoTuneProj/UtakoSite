from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.views import generic
from django_registration.backends.activation.views import RegistrationView, ActivationView
from django.urls import reverse_lazy

from .forms import (
    LoginForm,
    ResetPasswordForm,
    UtakoRegistrationForm,
    ResetPasswordConfirmForm,
    ChangePasswordForm,
)

class Login(LoginView):
    form_class = LoginForm
    template_name = 'register/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'register/logout.html'

class PasswordReset(PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'register/password_reset.html'
    email_template_name = 'register/password_reset_email.html'
    subject_template_name = 'register/password_reset_subject.html'
    success_url = reverse_lazy( 'register:password_reset_done' )

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'register/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = ResetPasswordConfirmForm
    template_name = 'register/password_reset_confirm.html'
    success_url = reverse_lazy('register:password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'

class PasswordChange(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'register/password_change.html'
    success_url = reverse_lazy( 'register:password_change_done' )

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'register/password_change_done.html'

class Registration(RegistrationView):
    form_class = UtakoRegistrationForm
    template_name = 'register/register.html'
    email_body_template = 'register/activation_email.txt'
    email_subject_template = 'register/activation_email_subject.txt'
    disallowed_url = reverse_lazy('register:register')
    success_url = reverse_lazy('register:login')

class Activation(ActivationView):
    template_name = 'register/activation_failed.html'
    success_url = reverse_lazy('register:login')
    def activate(self, request, *args, **kwargs):
        return super().activate(request, activation_key = request.GET.get('activation_key'))
