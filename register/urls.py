from django.urls import path, include

from . import views

app_name = 'register'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Registration.as_view(), name='register'),
    path('activate/', views.Activation.as_view(), name='activate'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
]
