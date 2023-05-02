from django.test import TestCase

from ..models import User, Group, Post, Comment, Follow
from ..models import POST_DATA, COMMENT_DATA, FOLLOW_DATA


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author_comment = User.objects.create(username='AuthorComment')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост - текст',
            author=cls.user,
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            text='Текст комментария',
            author=cls.author_comment,
            post=cls.post,
        )
        cls.follow = Follow.objects.create(
            user=cls.author_comment,
            author=cls.user,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей Post, Group, Comment
        корректно работает __str__."""
        correct_object_names = {
            self.group: self.group.title,
            self.post: POST_DATA.format(
                text=self.post.text,
                date=self.post.pub_date,
                author=self.post.author.username,
                group=self.post.group),
            self.comment: COMMENT_DATA.format(
                text=self.comment.text,
                date=self.comment.pub_date,
                author=self.author_comment.username,
                post=self.post.text),
            self.follow: FOLLOW_DATA.format(
                user=self.author_comment.username,
                author=self.user.username
            )
        }
        for object_name, expected_value in correct_object_names.items():
            with self.subTest(type(object_name).__name__):
                self.assertEqual(str(object_name), expected_value)
