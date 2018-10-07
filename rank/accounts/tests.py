from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.core.management import call_command
from django.urls import reverse

from accounts.models import Account


class TestUserManagement(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.model = Account

        self.superuser = self.model.objects.create_superuser('gb2@gb.ru', 'geekshop')

    def test_user_login(self):
        user = self.model.objects.create_user('test@test.ru', 'test', is_active=True)

        response = self.client.get(reverse('accounts:sign-in'))
        self.assertTrue(response.context['user'].is_anonymous)

        # login
        self.client.login(username='test@test.ru', password='test')
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], user)

        # company
        response = self.client.get('/company/view/2')
        self.assertEqual(response.context['user'], user)

        # cart
        response = self.client.get('/order/add/')
        self.assertContains(response, user, status_code=200)

    def test_user_logout(self):
        # self.user_with__first_name = self.model.objects.create_user('test_name@test.ru',
        #                                                             'test_name',
        #                                                             first_name='Фирст Нейм')
        #
        # # login
        # self.client.login(username='test_name@test.ru', password='test_name')
        #
        # response = self.client.get(reverse('accounts:sign-in'))
        # self.assertEqual(response.status_code, 302)
        #
        # response = self.client.get('/')
        # self.assertEqual(response.status_code, 200)
        # self.assertFalse(response.context['user'].is_anonymous)
        # self.assertEqual(response.context['user'], self.user_with__first_name)
        # self.assertEqual(response.context['user'].first_name, self.user_with__first_name.first_name)

        # logout
        response = self.client.get(reverse('accounts:sign-out'))
        self.assertEqual(response.status_code, 302)

        # main
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):
        response = self.client.get(reverse('accounts:sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        user = {
            'first_name': 'test',
            'email': 'test@test.ru',
            'password1': 'geekshop123',
            'password2': 'geekshop123',
        }

        response = self.client.post(reverse('accounts:sign-up'), data=user)
        self.assertEqual(response.status_code, 302)
        added_user = Account.objects.get(email=user['email'])
        activation_url = f"{settings.DOMAIN_NAME}/accounts/verify/{user['email']}/{added_user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        # login
        self.client.login(username=user['email'], password=user['password1'])

        response = self.client.get(reverse('accounts:sign-up'))
        self.assertEqual(response.status_code, 302)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, user['first_name'], status_code=200)

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
