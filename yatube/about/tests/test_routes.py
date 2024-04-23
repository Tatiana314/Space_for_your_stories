from django.test import TestCase
from django.urls import reverse

from ..urls import app_name


class RouteTests(TestCase):
    def test_routers(self):
        """Проверка маршрутов."""
        input_datas = [
            ['/about/author/', 'author'],
            ['/about/tech/', 'tech'],
        ]
        for address, route_name in input_datas:
            with self.subTest():
                self.assertEqual(
                    address,
                    reverse(f'{app_name}:{route_name}')
                )
