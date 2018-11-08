import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User, AnonymousUser

@pytest.mark.django_db
class TestRegister():
    def test_legal_change(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        c.force_login(user, backend='django.contrib.auth.backends.ModelBackend')
        token = c.get('/auth/password_change/').context['csrf_token']
        response = c.post('/auth/password_change/', {
            'old_password': 'mikuhatsune',
            'new_password1': 'mikuhachune',
            'new_password2': 'mikuhachune',
            'csrfmiddlewaretoken': str( token ),
        }, follow=True)
        assert User.objects.get(username='miku').check_password('mikuhachune')

    def test_illegal_change(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        c.force_login(user, backend='django.contrib.auth.backends.ModelBackend')
        token = c.get('/auth/password_change/').context['csrf_token']
        response = c.post('/auth/password_change/', {
            'old_password': 'mikuhachune',
            'new_password1': 'mikuhatsune',
            'new_password2': 'mikuhatsune',
            'csrfmiddlewaretoken': str( token ),
        }, follow=True)
        assert User.objects.get(username='miku').check_password('mikuhatsune')

    def test_anonymous(self):
        c = Client()
        response = c.get('/auth/password_change/')
        assert response.status_code == 302
