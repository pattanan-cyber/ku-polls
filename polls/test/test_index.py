"""ku polls index test"""
from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


def create_question(self, question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects \
        .create(question_text=question_text, pub_date=time)
class QuestionIndexViewTests(TestCase):
    """question index view"""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

