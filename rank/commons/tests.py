from django.test import TestCase
from django.test.client import Client
from rank_item.models import Company, CompanyCategory
from django.core.management import call_command


class TestRankItem(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/accounts/sign_in/')
        print('2'*200)
        print(response.context['user'])
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/order/add/')
        self.assertEqual(response.status_code, 302)

        for company in Company.objects.all():
            response = self.client.get(f'/company/view/{company.pk}')
            self.assertEqual(response.status_code, 200)

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
