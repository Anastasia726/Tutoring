from django.db import models

import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Task_theme(models.Model):
	theme_name = models.CharField('тема задания', max_length = 50)

	def __str__(self):
		return self.theme_name

class Task(models.Model):
	theme_name = models.ForeignKey(Task_theme, on_delete = models.CASCADE)
	task_title = models.CharField('название задания', max_length = 200)
	task_text = models.TextField('текст задания')
	correct_solution = models.TextField('правильное решение')
	pub_date = models.DateTimeField('дата публикации')

	def __str__(self):
		return self.task_title

	def was_published_recently(self):
		return self.pub_date >= (timezone.now() -  datetime.timedelta(days = 7))


class Solution(models.Model):
	user_name = models.ForeignKey(User, on_delete = models.CASCADE)
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	correct = models.SmallIntegerField('правильность решения', default = 0)

	def __str__(self):
		return str(self.user_name)
		

class Comment(models.Model):
	task = models.ForeignKey(Task, on_delete = models.CASCADE)
	author_name = models.ForeignKey(User, on_delete = models.CASCADE)
	comment_text = models.CharField('текст комментария', max_length = 200)
	comment_pub_date = models.DateTimeField('дата публикации')

	def __str__(self):
		return self.comment_text


class Search(models.Model):
	user_name = models.ForeignKey(User, related_name = "search_set", on_delete = models.CASCADE)
	search_text = models.CharField('текст запроса', max_length = 200)
	search_date = models.DateTimeField('дата запроса')

	def __str__(self):
		return self.search_text


class Message(models.Model):
	user_name = models.CharField('имя отправителя', max_length = 200)
	email = models.CharField('email', max_length = 200)
	message_text = models.TextField('текст сообщения')
	send_date = models.DateTimeField('дата отправления')

	def __str__(self):
		return self.user_name