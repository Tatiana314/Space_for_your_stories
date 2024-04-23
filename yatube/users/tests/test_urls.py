from django.contrib import auth
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import User

USERNAME = 'auth'
TOKEN = 'token'
UID = 'uidb64'
INDEX = reverse('posts:index')
SIGNUP = reverse('users:signup')
LOGOUT = reverse('users:logout')
LOGIN = reverse('users:login')
PASSWORD_CHANGE = reverse('users:password_change')
PASSWORD_CHANGE_DONE = reverse('users:password_change_done')
PASSWORD_RESET = reverse('users:password_reset')
PASSWORD_RESET_DONE = reverse('users:password_reset_done')
PASSWORD_RESET_CONFIRM = reverse(
    'users:password_reset_confirm', kwargs={'uidb64': UID, 'token': TOKEN}
)
PASSWORD_RESET_COMPLETE = reverse('users:password_reset_complete')
REDIRECT_PASSWORD_CHANGE = f'{LOGIN}?next={PASSWORD_CHANGE}'
REDIRECT_CHANGE_DONE = f'{LOGIN}?next={PASSWORD_CHANGE_DONE}'


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest = Client()
        cls.another = Client()
        cls.author_client = Client()
        cls.author = User.objects.create(username=USERNAME)
        cls.user = User.objects.create_user(username='NoName')

    def setUp(self):
        self.another.force_login(self.user)
        self.author_client.force_login(self.author)

    def test_page_status_code(self):
        """Доступ страниц пользователям."""
        cases = [
            [SIGNUP, self.guest, 200],
            [LOGIN, self.guest, 200],
            [LOGOUT, self.author_client, 200],
            [PASSWORD_CHANGE, self.another, 200],
            [PASSWORD_CHANGE_DONE, self.another, 200],
            [PASSWORD_CHANGE, self.guest, 302],
            [PASSWORD_CHANGE_DONE, self.guest, 302],
            [LOGOUT, self.guest, 200],
            [PASSWORD_RESET, self.guest, 200],
            [PASSWORD_RESET_DONE, self.guest, 200],
            [PASSWORD_RESET_CONFIRM, self.guest, 200],
            [PASSWORD_RESET_COMPLETE, self.guest, 200],
            [PASSWORD_RESET, self.another, 200],
            [PASSWORD_RESET_DONE, self.another, 200],
            [PASSWORD_RESET_CONFIRM, self.another, 200],
            [PASSWORD_RESET_COMPLETE, self.another, 200]
        ]
        for adress, client, code in cases:
            with self.subTest(
                code=code, adress=adress, client=auth.get_user(client).username
            ):
                self.assertEqual(
                    client.get(adress).status_code, code
                )

    def test_users_urls_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cases = [
            [SIGNUP, self.guest, 'users/signup.html'],
            [LOGOUT, self.author_client, 'users/logged_out.html'],
            [LOGIN, self.guest, 'users/login.html'],
            [PASSWORD_CHANGE, self.another, 'users/password_change_form.html'],
            [
                PASSWORD_CHANGE_DONE, self.another,
                'users/password_change_done.html'
            ],
            [PASSWORD_RESET, self.guest, 'users/password_reset_form.html'],
            [
                PASSWORD_RESET_DONE, self.guest,
                'users/password_reset_done.html'
            ],
            [
                PASSWORD_RESET_CONFIRM, self.guest,
                'users/password_reset_confirm.html'
            ],
            [
                PASSWORD_RESET_COMPLETE, self.guest,
                'users/password_reset_complete.html'
            ],
        ]
        for adress, client, template in cases:
            with self.subTest(adress=adress):
                self.assertTemplateUsed(
                    client.get(adress), template
                )

    def test_user_urls_redirect_anonymous_client(self):
        """Перенаправление пользователей."""
        input_data = [
            [PASSWORD_CHANGE, self.guest, REDIRECT_PASSWORD_CHANGE],
            [PASSWORD_CHANGE_DONE, self.guest, REDIRECT_CHANGE_DONE],
        ]
        for adress, client, new_adress in input_data:
            with self.subTest(
                client=auth.get_user(client).username,
                adress=adress,
                new_adress=new_adress
            ):
                self.assertRedirects(
                    client.get(adress, follow=True),
                    new_adress
                )
