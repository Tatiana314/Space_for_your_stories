from django.test import TestCase
from django.urls import reverse

from ..urls import app_name

TOKEN = 'token'
UID = 'uidb64'


class RouteTest(TestCase):
    def tests_routers(self):
        """Проверка маршрутов."""
        input_datas = [
            ['/auth/signup/', 'signup'],
            ['/auth/logout/', 'logout'],
            ['/auth/login/', 'login'],
            ['/auth/password_change/', 'password_change'],
            ['/auth/password_change/done/', 'password_change_done'],
            ['/auth/password_reset/', 'password_reset'],
            ['/auth/password_reset/done/', 'password_reset_done'],
            [
                f'/auth/reset/{UID}/{TOKEN}/',
                'password_reset_confirm',
                UID,
                TOKEN
            ],
            ['/auth/reset/done/', 'password_reset_complete'],
        ]
        for address, route_name, *arguments in input_datas:
            with self.subTest():
                self.assertEqual(
                    address,
                    reverse(f'{app_name}:{route_name}', args=arguments)
                )
