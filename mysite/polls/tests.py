from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Question
# Create your tests here.

def create_question(question_text,days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        # checks if publishing date is today or older
        # returns false if date is > today
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_recently_with_old_question(self):
        # should return false for questions prior to the last 24 hours
        time = timezone.now() - datetime.timedelta(seconds=86401)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)

    def test_was_published_recently_with_recent_question(self):
        # should return true if within the day
        time = timezone.now() - datetime.timedelta(seconds=86399)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        # display a message if no questions exist
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        # checks if historicaly published questions are displayed which they should be
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_future_question(self):
        # checks to see if future questions are not displayed
        create_question(question_text='Future question.',days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        # checks to ensure only historical questions are presented even when both exist
        create_question(question_text="Future question.",days=30)
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_two_past_questions(self):
        # Ensures that multiple old questions are also filtered
        create_question(question_text="Past question 1.",days=-30)
        create_question(question_text="Past question 2.",days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

