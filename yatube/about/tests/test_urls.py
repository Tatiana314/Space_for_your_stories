from django.test import Client, TestCase
from django.urls import reverse

AUTHOR = reverse('about:author')
TECH = reverse('about:tech')


class StaticPagesURLTests(TestCase):
    url_names = {
        'about/author.html': AUTHOR,
        'about/tech.html': TECH,
    }

    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Доступность статических страниц любому клиенту."""
        for adress in self.url_names.values():
            with self.subTest():
                self.assertEqual(
                    self.guest_client.get(adress).status_code, 200)

    def test_about_url_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон статических страниц."""
        for template, adress in self.url_names.items():
            with self.subTest():
                self.assertTemplateUsed(
                    self.guest_client.get(adress), template)
