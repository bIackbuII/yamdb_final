from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser

from .validators import year_validator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE = ((USER, 'User'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=100,
        blank=True,
        choices=USER_ROLE,
        default=USER
    )

    confirmation_code = models.CharField(
        verbose_name='Проверочный код',
        max_length=100,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(
        max_length=10, verbose_name='Категория произведения')
    slug = models.SlugField(unique=True, verbose_name='Описание категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=10, verbose_name='Жанр произведения')
    slug = models.SlugField(unique=True, verbose_name='Описание жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(
        max_length=50, db_index=True, verbose_name='Наименование произведения')
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[year_validator])
    description = models.TextField(
        max_length=200, verbose_name='Описание произведения')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр произведения')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category_titles',
        null=True,
        blank=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        null=True,
        db_index=True,
        verbose_name='Произведение')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews_author',
        verbose_name='Автор отзыва')
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка отзыва',
        validators=[MinValueValidator(1,
                    message='Значение не может быть менее 1'),
                    MaxValueValidator(10,
                    message='Значение не может быть более 10')])
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='single_review_per_user'),
        ]
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True,
        verbose_name='Отзыв')
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="comment_username",
        verbose_name='Автор комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
