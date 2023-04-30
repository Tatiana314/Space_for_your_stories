from django.test import TestCase, Client
from django.urls import reverse

from ..models import User, Group, Post

SLUG = 'test_slug'
USERNAME = 'auth'
INDEX = reverse('posts:index')
GROUP_LIST = reverse('posts:group_list', args=[SLUG])
PROFILE = reverse('posts:profile', args=[USERNAME])
POST_CREATE = reverse('posts:post_create')
UNEXIST_PAGE = '/unexist_page/'
LOGIN = reverse('users:login')
PROFILE_FOLLOW = reverse('posts:profile_follow', args=[USERNAME])
PROFILE_UNFOLLOW = reverse('posts:profile_unfollow', args=[USERNAME])
FOLLOW = reverse('posts:follow_index')


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username=USERNAME)
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title=('Заголовок тестовой группы'),
            slug=SLUG
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
            group=cls.group,
        )
        cls.POST_EDIT = reverse('posts:post_edit', args=[cls.post.id])
        cls.POST_DETAIL = reverse('posts:post_detail', args=[cls.post.id])
        cls.REDIRECT_POST_CREATE = f'{LOGIN}?next={POST_CREATE}'
        cls.REDIRECT_POST_EDIT = f'{LOGIN}?next={cls.POST_EDIT}'
        cls.ADD_COMMENT = reverse('posts:add_comment', args=[cls.post.id])
        cls.REDIRECT_ADD_COMMENT = f'{LOGIN}?next={cls.ADD_COMMENT}'

    def setUp(self):
        self.guest = Client()
        self.another = Client()
        self.another.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_url_exists_at_desired_location_unauthorized_client(self):
        """Доступ страниц пользователям."""
        cases = [
            [INDEX, self.guest, 200],
            [GROUP_LIST, self.guest, 200],
            [PROFILE, self.guest, 200],
            [self.POST_DETAIL, self.guest, 200],
            [UNEXIST_PAGE, self.guest, 404],
            [self.POST_EDIT, self.author_client, 200],
            [POST_CREATE, self.another, 200],
            [POST_CREATE, self.guest, 302],
            [self.POST_EDIT, self.guest, 302],
            [self.POST_EDIT, self.another, 302],
            [self.ADD_COMMENT, self.guest, 302],
            [PROFILE_FOLLOW, self.another, 302],
            [PROFILE_UNFOLLOW, self.another, 302],
            [FOLLOW, self.another, 200],
        ]
        for adress, client, code in cases:
            with self.subTest(code=code):
                self.assertEqual(
                    client.get(adress).status_code, code
                )

    def test_posts_urls_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cases = [
            [self.POST_EDIT, self.author_client, 'posts/create_post.html'],
            [INDEX, self.another, 'posts/index.html'],
            [GROUP_LIST, self.another, 'posts/group_list.html'],
            [PROFILE, self.another, 'posts/profile.html'],
            [self.POST_DETAIL, self.another,
             'posts/post_detail.html'],
            [POST_CREATE, self.another, 'posts/create_post.html'],
            [FOLLOW, self.another, 'posts/follow.html'],
        ]
        for adress, client, template in cases:
            with self.subTest(adress=adress):
                self.assertTemplateUsed(
                    client.get(adress), template
                )

    def test_posts_urls_redirect_anonymous_client(self):
        """Перенаправление пользователей."""
        input_data = [
            [POST_CREATE, self.guest, self.REDIRECT_POST_CREATE],
            [self.POST_EDIT, self.guest, self.REDIRECT_POST_EDIT],
            [self.POST_EDIT, self.another, self.POST_DETAIL],
            [self.ADD_COMMENT, self.guest, self.REDIRECT_ADD_COMMENT],
            [PROFILE_FOLLOW, self.another, PROFILE],
            [PROFILE_UNFOLLOW, self.another, PROFILE],
        ]
        for adress, client, new_adress in input_data:
            with self.subTest(new_adress=new_adress):
                self.assertRedirects(
                    client.get(adress, follow=True),
                    new_adress,
                    status_code=302
                )
