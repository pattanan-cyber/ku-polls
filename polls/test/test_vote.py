from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question


class VotesTests(TestCase):
    """Test vote"""
    def test_this_question_is_can_vote(self):
        """The question can vote if it still on time.
        It should return True."""
        time = timezone.now() - datetime.timedelta(seconds=1)
        question = Question(pub_date=time)
        self.assertTrue(question.can_vote())

    def test_this_question_is_can_not_vote(self):
        """The question can not vote if it still on time.
        It should return True."""
        time = timezone.now() + datetime.timedelta(hours=20)
        end = timezone.now() + datetime.timedelta(hours=1)
        question_can_not_vote = Question(pub_date=end, end_date=time)
        self.assertIs(question_can_not_vote.can_vote(), False)