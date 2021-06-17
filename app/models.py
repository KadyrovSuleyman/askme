from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
from django.db.models import indexes

import time


# Create your models here.


class Profile(models.Model):
    nickname = models.CharField(max_length=256, verbose_name='Никнейм')
    avatar = models.ImageField(default='static/img/200.jpg', verbose_name='Аватар', upload_to='static/img')
    user = models.OneToOneField(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# --------------------------------------------

class AuthorManager(models.Manager):

    def calc_rating(self):
        time.sleep(5)
        return ['user1', 'user2']


class Author(models.Model):
    avatar = models.ImageField(
        upload_to='avatar/%Y/%m/%d', default='avatar.jpg')
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = AuthorManager()


# --------------------------------------------

class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-date_created')

    def hot(self):
        return self.all().order_by('-rating')

    def find_by_tag(self, tag):
        return self.filter(tags__name=tag)

    def find_by_pk(self, question_pk):
        return self.get(pk=question_pk)


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст вопроса')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    tags = models.ManyToManyField('Tag', verbose_name='Теги')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        indexes = [models.Index(fields=['rating']),
                   models.Index(fields=['date_created'])]


class AnswerManager(models.Manager):
    def find_by_question(self, question):
        return self.filter(question=question).order_by('-rating')


class Answer(models.Model):
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(
        verbose_name='Правильный ответ', default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    objects = AnswerManager()

    def __str__(self):
        return self.question.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        indexes = [models.Index(fields=['rating'])]


class TagManager(models.Model):
    def best(self):
        return self.all()[:10]


class Tag(models.Model):
    name = models.CharField(max_length=1024, unique=True, verbose_name='Тэг')

    objects = TagManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES = {(LIKE, 'like'), (DISLIKE, 'dislike')}
    ACTIONS = {x[1]: x[0] for x in CHOICES}
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    value = models.IntegerField()


class AnswerVote(models.Model):
    LIKE = 1
    DISLIKE = -1
    CHOICES = {(LIKE, 'like'), (DISLIKE, 'dislike')}
    ACTIONS = {x[1]: x[0] for x in CHOICES}
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    value = models.IntegerField()