from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from core.models import CreatedModel


User = get_user_model()
POST_DATA = '{text:.15}, {date:%Y-%m-%d}, {author}, {group}'
COMMENT_DATA = '{text:.15}, {date:%Y-%m-%d}, {author}, {post:.15}'
FOLLOW_DATA = '{user} подписан на {author}'


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Метка'
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=settings.IMAGES_DIRECTORY,
        blank=True,
        null=True
    )

    class Meta(CreatedModel.Meta):
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return POST_DATA.format(
            text=self.text,
            date=self.pub_date,
            author=self.author.username,
            group=self.group
        )


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст нового комментария',
    )

    class Meta(CreatedModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return COMMENT_DATA.format(
            text=self.text,
            date=self.pub_date,
            author=self.author.username,
            post=self.post.text
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=False,
        related_name='following',
        verbose_name='Автор постов',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return FOLLOW_DATA.format(
            user=self.user.username,
            author=self.author.username
        )
