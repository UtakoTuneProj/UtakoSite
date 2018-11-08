import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User, AnonymousUser

@pytest.mark.django_db
class TestRegister():
    def test_legal_login(self):
        c = Client()
        token = c.get('/auth/register/').context['csrf_token']
        response = c.post('/auth/register/', {
            'username': 'miku',
            'email': 'miku@example.com',
            'password1': 'mikuhatsune',
            'password2': 'mikuhatsune',
            'csrfmiddlewaretoken': str( token ),
        }, follow=True)
        assert User.objects.filter(username='miku').count() == 1
    def test_short_password(self):
        c = Client()
        token = c.get('/auth/register/').context['csrf_token']
        response = c.post('/auth/register/', {
            'username': 'miku',
            'email': 'miku@example.com',
            'password1': 'miku',
            'password2': 'miku',
            'csrfmiddlewaretoken': str( token ),
        }, follow=True)
        assert User.objects.filter(username='miku').count() == 0
    def test_password_not_same(self):
        c = Client()
        token = c.get('/auth/register/').context['csrf_token']
        response = c.post('/auth/register/', {
            'username': 'miku',
            'email': 'miku@example.com',
            'password1': 'miku',
            'password2': 'mikumiku',
            'csrfmiddlewaretoken': str( token ),
        }, follow=True)
        assert User.objects.filter(username='miku').count() == 0
