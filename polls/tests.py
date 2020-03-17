import datetime

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice


class QuestionModelTests(TestCase):

    def test_how_many_choices_with_two(self):
        question = Question(question_text='test_question', pub_date=timezone.now())
        question.save()
        choice1 = Choice(choice_text='choice1', question=question)
        choice1.save()
        choice2 = Choice(choice_text='choice1', question=question)
        choice2.save()
        self.assertEqual(question.how_many_choices(), 2)

    def test_how_many_choices_with_zero(self):
        question = Question(question_text='test_question', pub_date=timezone.now())
        question.save()
        self.assertEqual(question.how_many_choices(), 0)


class IndexViewTest(TestCase):

    def test_question_without_question_mark(self):
        Question.objects.create(question_text='Question!', pub_date=timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_with_question_mark(self):
        Question.objects.create(question_text='Question?', pub_date=timezone.now())
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Question?>'])
