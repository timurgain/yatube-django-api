from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Table with posts."""
    text = models.TextField(
        help_text='Начните здесь статью',
        verbose_name='Статья',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор статьи',
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        help_text='Загрузите картинку',
        verbose_name='Картинка для статьи',
    )
    group = models.ForeignKey(
        to='Group',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Выбери группу/сообщество',
        verbose_name='Сообщество',
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f"{self.id}: {self.text[0:30]}"


class Group(models.Model):
    """Table with groups."""
    title = models.CharField(
        max_length=200,
        verbose_name='Сообщество',
    )
    slug = models.SlugField(
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Table with comments."""
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    text = models.TextField(
        verbose_name='Комментарий',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f"{self.text[0:30]}..., {self.author}"


class Follow(models.Model):
    """Table with subscriptions."""
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='following',
        verbose_name='Автор статьи',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user} подписан на автора {self.author}'
