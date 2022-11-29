from django.contrib.auth.models import User
from django.db import models


class ToDo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название задачи')
    text = models.TextField(verbose_name='Описание задачи', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Задача создана')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    deadline = models.DateTimeField(null=True, verbose_name='Срок сдачи')
    important = models.BooleanField(default=False, verbose_name='Важность задачи')


    def __str__(self):
        return self.title