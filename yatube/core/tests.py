from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        self.assertEqual(self.client.get('/nonexist-page/').status_code, 404)
        self.assertTemplateUsed(
            self.client.get('/nonexist-page/'), 'core/404.html'
        )
