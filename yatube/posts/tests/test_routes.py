from django.test import TestCase
from django.urls import reverse

from ..urls import app_name


SLUG = 'slug'
USERNAME = 'username'
POST_ID = 1


class RouteTests(TestCase):
    def test_routers(self):
        """Проверка маршрутов."""
        input_datas = [
            ['/', 'index'],
            [f'/group/{SLUG}/', 'group_list', SLUG],
            [f'/profile/{USERNAME}/', 'profile', USERNAME],
            [f'/posts/{POST_ID}/edit/', 'post_edit', POST_ID],
            [f'/posts/{POST_ID}/', 'post_detail', POST_ID],
            ['/create/', 'post_create'],
            [f'/posts/{POST_ID}/comment/', 'add_comment', POST_ID],
            ['/follow/', 'follow_index'],
            [f'/profile/{USERNAME}/follow/', 'profile_follow', USERNAME],
            [f'/profile/{USERNAME}/unfollow/', 'profile_unfollow', USERNAME],
        ]
        for address, route_name, *arguments in input_datas:
            with self.subTest():
                self.assertEqual(
                    address,
                    reverse(f'{app_name}:{route_name}', args=arguments)
                )
