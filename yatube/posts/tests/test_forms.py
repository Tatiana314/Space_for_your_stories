import shutil
import tempfile

from django import forms
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ..models import User, Post, Group, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
USERNAME = 'auth'
LOGIN = reverse('users:login')
IMAGES_DIRECTORY = Post._meta.get_field('image').upload_to
SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
PROFILE = reverse('posts:profile', args=[USERNAME])
POST_CREATE = reverse('posts:post_create')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest = Client()
        cls.another = Client()
        cls.author_client = Client()
        cls.author = User.objects.create(username=USERNAME)
        cls.user = User.objects.create_user(username='NoName')
        cls.group_1 = Group.objects.create(
            title=('Заголовок для тестовой группы 1'),
            slug='test_slug_1'
        )
        cls.group_2 = Group.objects.create(
            title=('Заголовок для тестовой группы 2'),
            slug='test_slug_2'
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            group=cls.group_1,
            author=cls.author,
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        cls.uploaded_2 = SimpleUploadedFile(
            name='small_2.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        cls.uploaded_3 = SimpleUploadedFile(
            name='small_3.gif',
            content=SMALL_GIF,
            content_type='image/gif'
        )
        cls.POST_EDIT = reverse('posts:post_edit', args=[cls.post.id])
        cls.POST_DETAIL = reverse('posts:post_detail', args=[cls.post.id])
        cls.ADD_COMMENT = reverse('posts:add_comment', args=[cls.post.id])
        cls.REDIRECT_POST_CREATE = f'{LOGIN}?next={POST_CREATE}'
        cls.REDIRECT_POST_EDIT = f'{LOGIN}?next={cls.POST_EDIT}'
        cls.REDIRECT_ADD_COMMENT = f'{LOGIN}?next={cls.ADD_COMMENT}'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.another.force_login(self.user)
        self.author_client.force_login(self.author)

    def test_forms_create_post(self):
        """Валидная форма создает запись в Post."""
        posts = set(Post.objects.all())
        form_data = {
            'text': 'Тестовый пост 2',
            'group': self.group_1.id,
            'image': self.uploaded,
        }
        response = self.author_client.post(
            POST_CREATE,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, PROFILE)
        posts = set(Post.objects.all()) - posts
        self.assertEqual(len(posts), 1)
        post = posts.pop()
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.author)
        self.assertEqual(
            post.image.name,
            '{}{}'.format(IMAGES_DIRECTORY, form_data['image'].name)
        )

    def test_create_post_pages_show_correct_context(self):
        """Типы полей формы create_post / post_edit / post_detail_comment
        в словаре context соответствуют ожиданиям"""
        field_values = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        cases = (
            (self.another, POST_CREATE, ('text', 'group', 'image')),
            (self.author_client, self.POST_EDIT, ('text', 'group', 'image')),
            (self.another, self.POST_DETAIL, ('text',))
        )
        for site_user, address, form_fields in cases:
            response = site_user.get(address)
            for value in form_fields:
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, field_values[value])

    def test_forms_edit_post(self):
        """Проверка формы редактирования поста и изменение
        его в базе данных."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Измененный тестовый пост',
            'group': self.group_2.id,
            'image': self.uploaded_2,
        }
        response = self.author_client.post(
            self.POST_EDIT,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.POST_DETAIL)
        self.assertEqual(Post.objects.count(), posts_count)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(
            post.image.name,
            '{}{}'.format(IMAGES_DIRECTORY, form_data['image'].name)
        )

    def test_authorized_user_can_comment(self):
        """Авторизированный пользователь может комментировать"""
        comments = set(Comment.objects.all())
        form_data = {
            'text': 'Тестовый комментарий',
        }
        response = self.another.post(
            self.ADD_COMMENT,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.POST_DETAIL)
        comments = set(Comment.objects.all()) - comments
        self.assertEqual(len(comments), 1)
        comment = comments.pop()
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_an_unauthorized_user_cannot_comment(self):
        """Неавторизированный пользователь не может комментировать."""
        comments = set(Comment.objects.all())
        form_data = {
            'text': 'Тестовый комментарий',
        }
        response = self.guest.post(
            self.ADD_COMMENT,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.REDIRECT_ADD_COMMENT)
        self.assertFalse(set(Comment.objects.all()) - comments)

    def test_an_unauthorized_user_cannot_create_a_post(self):
        """Неавторизированный пользователь не может создать пост."""
        posts = set(Post.objects.all())
        form_data = {
            'text': 'Тестовый пост неавторизированного пользователя',
            'group': self.group_2.id,
            'image': self.uploaded_3,
        }
        response = self.guest.post(
            POST_CREATE,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.REDIRECT_POST_CREATE)
        self.assertFalse(set(Post.objects.all()) - posts)

    def test_an_unauthorized_user_cannot_edit_a_post(self):
        """Неавторизированный пользователь не может редактировать пост."""
        posts = set(Post.objects.values_list('id', 'text', 'group'))
        cases = [
            (self.guest, self.REDIRECT_POST_EDIT),
            (self.another, self.POST_DETAIL)
        ]
        form_data = {
            'text': 'Измененный пост',
            'group': self.group_2.id,
            'image': self.uploaded_3
        }
        for client, route in cases:
            response = client.post(
                self.POST_EDIT,
                data=form_data,
                follow=True
            )
            with self.subTest(client=client):
                self.assertRedirects(response, route)
                self.assertEqual(
                    set(Post.objects.values_list('id', 'text', 'group')), posts
                )
