import datetime

from django.db import models

class Poll(models.Model):

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, default=None)
    is_active = models.BooleanField(default=True)

class Question(models.Model):
    question_types = (
        ('TEXT', 'Free Text'),
        ('ONE', 'One from list'),
        ('MANY', 'Many from list'),)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=256)
    type = models.CharField(max_length=128, choices=question_types, default=question_types[0])


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default=None, blank=False)

class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    many = models.ManyToManyField(Choice, related_name='answers', blank=True)
    one = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=128, blank=True, null=True)
    user = models.IntegerField(blank=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'poll', 'question'], name='unique answer')]