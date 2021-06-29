from django.test import TestCase
from.models import Shortener
from django.urls import reverse
from django.test import Client
from django.core.exceptions import ValidationError


class TestShortener(TestCase):

    def setUp(self):
        self.shortener = Shortener.objects.create(full_url='https://pcentra.com/')
        self.short_url = self.shortener.short_url
        self.client = Client()

    def test_create_and_redirect(self):
        url = reverse('create')
        response = self.client.post(url, {'url': 'https://www.djangoproject.com/'}, content_type='application/json')
        shortener_dict = response.json()
        shortener = Shortener.objects.get(id=shortener_dict['id'])
        short_url = shortener.short_url
        url = reverse('redirect', args=[short_url])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_non_existing_short_url(self):
        url = reverse('redirect', args=[self.short_url + 'x'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_success_create_shortener(self):
        url = reverse('create')
        response = self.client.post(url, {'url': 'https://www.djangoproject.com/'}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_shortener_existing_short_url(self):
        try:
            shortener = Shortener.objects.create(full_url='https://pcentra.com/', short_url=self.short_url)
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'short_url': ['Shortener with this Short url already exists.']})

    def test_create_invalid_full_url(self):
        try:
            shortener = Shortener.objects.create(full_url='dsghdfgjgku')
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'full_url': ['Enter a valid URL.']})

    def test_counter_increament(self):
        counter_before = self.shortener.counter
        short_url = self.shortener.short_url
        url = reverse('redirect', args=[short_url])
        self.client.get(url)
        counter_after = Shortener.objects.get(id=self.shortener.id).counter
        self.assertEqual(counter_before + 1, counter_after)



