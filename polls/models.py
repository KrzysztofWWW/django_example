import datetime

from django.db import models

# Create your models here.
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        if self.pub_date >= timezone.now() - datetime.timedelta(days=1):
            if self.pub_date <= timezone.now():
                return True
        return False

    def how_many_choices(self):
        return self.choice_set.count()

    def ends_with_question_mark(self):
        return self.question_text.endswith('?')



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
