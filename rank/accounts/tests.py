from django.test import TestCase
from django.test import Client
from django.core.management import call_command
from django.urls import reverse
from django.test.utils import setup_test_environment, teardown_test_environment

from .models import Account


class TestUserManagement(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        model = Account

        self.superuser = model.objects.create_superuser('gb2@gb.ru', 'geekshop')
        self.user = model.objects.create_user('test@test.ru', 'test')
        self.user_with__first_name = model.objects.create_user('test_name@test.ru',
                                                               'test_name',
                                                               first_name='Фирст Нейм')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # response = self.client.get('/accounts/sign_in/')
        # self.assertTrue(response.context['user'].is_anonymous)

        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username='gb2@gb.ru', password='geekshop')

        # логинимся
        response = self.client.get(reverse('accounts:sign-in'))
        print(response)
        print(dir(response))
        # self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        # главная после логина
        # response = self.client.get('/')
        # self.assertContains(response, 'Пользователь', status_code=200)
        # self.assertEqual(response.context['user'], self.user)
        # self.assertIn('Пользователь', response.content.decode())

    def tearDown(self):
        call_command('sqlsequencereset',

                     'accounts',
                     'basket',
                     'commons',
                     'landing',
                     'orders',
                     'rank_admin',
                     'rank_item',
                     )
