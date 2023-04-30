from django.test import TestCase, Client


class StaticPagesURLTests(TestCase):
    url_names = {
        'about/author.html': '/about/author/',
        'about/tech.html': '/about/tech/',
    }

    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Доступность статических страниц любому клиенту."""
        for adress in self.url_names.values():
            with self.subTest():
                self.assertEqual(
                    self.guest_client.get(adress).status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона статических страниц."""
        for template, adress in self.url_names.items():
            with self.subTest():
                self.assertTemplateUsed(
                    self.guest_client.get(adress), template)
