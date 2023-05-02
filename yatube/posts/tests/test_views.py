from django.test import Client, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.core.cache import cache

from ..constants import POSTS_NUMBER
from ..models import User, Post, Group, Follow

REST_POSTS = 3
SLUG = 'test_slug'
SLUG_2 = 'test_slug_2'
USERNAME = 'auth'
INDEX = reverse('posts:index')
GROUP_LIST = reverse('posts:group_list', args=[SLUG])
PROFILE = reverse('posts:profile', args=[USERNAME])
GROUP_LIST_2 = reverse('posts:group_list', args=[SLUG_2])
PROFILE_FOLLOW = reverse('posts:profile_follow', args=[USERNAME])
PROFILE_UNFOLLOW = reverse('posts:profile_unfollow', args=[USERNAME])
FOLLOW = reverse('posts:follow_index')
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.another = Client()
        cls.author_client = Client()
        cls.author = User.objects.create(username=USERNAME)
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title=('Тестовая группа'),
            slug=SLUG,
            description='Описание группы'
        )
        cls.group_2 = Group.objects.create(
            title=('Заголовок для тестовой группы 2'),
            slug=SLUG_2
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.author,
            group=cls.group,
            image=cls.uploaded
        )
        cls.POST_DETAIL = reverse('posts:post_detail', args=[cls.post.id])

    def setUp(self):
        cache.clear()
        self.another.force_login(self.user)
        self.author_client.force_login(self.author)

    def test_index_group_detail_profile_pages_show_correct_context(self):
        """Шаблоны index, group_list, profile, post_detail, follow_index"""
        """сформированы с правильным контекстом."""
        pages = {
            INDEX: 'page_obj',
            GROUP_LIST: 'page_obj',
            PROFILE: 'page_obj',
            self.POST_DETAIL: 'post',
            FOLLOW: 'page_obj',

        }
        Follow.objects.create(user=self.user, author=self.author)
        for adress, context_element in pages.items():
            with self.subTest(adress=adress):
                response = self.another.get(adress)
                if context_element == 'page_obj':
                    self.assertIn(
                        self.post, response.context[context_element]
                    )
                    list_page_obj = (
                        response.context[context_element]
                    )
                    post = list_page_obj[list_page_obj.index(self.post)]
                else:
                    post = response.context.get('post')
                self.assertEqual(post.pk, self.post.pk)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)

    def test_post_not_appearing_not_subscribed(self):
        """Пост автора не появляется в ленте тех, кто не подписан."""
        self.assertNotIn(
            self.post,
            self.another.get(FOLLOW).context['page_obj']
        )

    def test_profile_pages_show_correct_context(self):
        """Автор в контексте Профиля."""
        self.assertEqual(
            self.another.get(PROFILE).context.get('author'), self.author
        )

    def test_group_list_pages_show_correct_context(self):
        """Группа в контексте Групп-ленты без искажения атрибутов."""
        response = self.another.get(GROUP_LIST)
        group = response.context.get('group')
        self.assertEqual(group.pk, self.group.pk)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.description, self.group.description)

    def test_cache_index(self):
        """Тест кэширования страницы index"""
        first_request = self.another.get(INDEX)
        post = first_request.context['page_obj'][0]
        Post.objects.filter(id=post.id).delete()
        second_request = self.another.get(INDEX)
        self.assertEqual(first_request.content, second_request.content)
        cache.clear()
        third_request = self.another.get(INDEX)
        self.assertNotEqual(first_request.content, third_request.content)

    def test_author_client_add_delete_subscription_to_the_author(self):
        """Авторизованный пользователь может подписываться
        на других пользователей."""
        follow_exists = Follow.objects.filter(
            user=self.user, author=self.author
        ).exists()
        self.another.get(PROFILE_FOLLOW)
        self.assertNotEqual(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            follow_exists
        )

    def test_author_client_add_delete_subscription_to_the_author(self):
        """Авторизованный пользователь может удалять авторов из подписки."""
        Follow.objects.create(user=self.user, author=self.author)
        follow_exists = Follow.objects.filter(
            user=self.user, author=self.author
        ).exists()
        self.another.get(PROFILE_UNFOLLOW)
        self.assertNotEqual(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            follow_exists
        )

    def test_paginator_count_posts(self):
        Post.objects.bulk_create(
            Post(
                author=self.author,
                text=f'Тестовый пост {count}',
                group=self.group,
            )
            for count in range(POSTS_NUMBER + REST_POSTS)
        )
        Follow.objects.create(user=self.user, author=self.author)
        rest_posts = Post.objects.count() - POSTS_NUMBER
        cases = [
            [INDEX, POSTS_NUMBER],
            [f'{INDEX}?page=2', rest_posts],
            [GROUP_LIST, POSTS_NUMBER],
            [f'{GROUP_LIST}?page=2', rest_posts],
            [PROFILE, POSTS_NUMBER],
            [f'{PROFILE}?page=2', rest_posts],
            [FOLLOW, POSTS_NUMBER],
            [f'{FOLLOW}?page=2', rest_posts]
        ]

        for url_1, number_posts in cases:
            with self.subTest(url_1=url_1):
                self.assertEqual(
                    len(self.another.get
                        (url_1).context['page_obj']),
                    number_posts
                )
