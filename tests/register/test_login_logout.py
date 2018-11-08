import pytest
from django.test import TestCase, Client
from django.contrib.auth.models import User, AnonymousUser

@pytest.mark.django_db
class TestLogIn():
    def test_legal_login(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        token = c.get('/auth/login/').context['csrf_token']
        response = c.post('/auth/login/', {'username': 'miku', 'password': 'mikuhatsune', 'csrfmiddlewaretoken': str( token )}, follow=True)
        assert response.context["user"].username == 'miku'

    def test_user_does_not_exist(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        token = c.get('/auth/login/').context['csrf_token']
        response = c.post('/auth/login/', {'username': 'rin', 'password': 'rinkagamine', 'csrfmiddlewaretoken': str( token )}, follow=True)
        assert response.context["user"].username == ''

    def test_password_not_collect(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        token = c.get('/auth/login/').context['csrf_token']
        response = c.post('/auth/login/', {'username': 'miku', 'password': 'mikuhachune', 'csrfmiddlewaretoken': str( token )}, follow=True)
        assert response.context["user"].username == ''

@pytest.mark.django_db
class TestLogOut():
    def test_legal_login(self):
        user = User.objects.create(
            username = 'miku',
            email = 'miku@example.com',
        )
        user.set_password('mikuhatsune')
        user.save()
        c = Client()
        c.force_login(user, backend='django.contrib.auth.backends.ModelBackend')
        response = c.get('/auth/logout/', follow=True)
        assert response.context["user"].username == ''
