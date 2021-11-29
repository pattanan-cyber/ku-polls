"""ku polls index test"""
from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(question_text, days):
    """Create a question with the given `question_text` and published date."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """question index view"""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        """Future question does not appear on index page."""
        create_question(question_text="Future question.", days=365)
        client = self.client.get(reverse('polls:index'))
        self.assertContains(client, "No polls are available.")
        self.assertQuerysetEqual(client.context['latest_question_list'], [])

    def test_past_question(self):
        """Index page displays past question."""
        q1 = create_question(question_text="Past question.", days=-1)
        client = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(client.context['latest_question_list'],[q1],)

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )