from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic

from .forms import LoginForm

class Login(LoginView):
    form_class = LoginForm
    template_name = 'register/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'register/logout.html'
