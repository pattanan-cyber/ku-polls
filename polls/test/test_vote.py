from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question


class VotesTests(TestCase):
    """Test vote"""
    def test_this_question_is_can_vote(self):
        """The question can vote if it still on time.
        It should return True."""
        time = timezone.now() - datetime.timedelta(hours=23)
        end = timezone.now() + datetime.timedelta(hours=2)
        time1 = timezone.now() - datetime.timedelta(minutes=50)
        end1 = timezone.now() + datetime.timedelta(hours=10)
        question_can_vote1 = Question(pub_date=end, end_date=time)
        self.assertIs(question_can_vote1.can_vote(), True)
        question_can_vote2 = Question(pub_date=end1, end_date=time1)
        self.assertIs(question_can_vote2.can_vote(), True)

    def test_this_question_is_can_not_vote(self):
        """The question can not vote if it still on time.
        It should return True."""
        time = timezone.now() + datetime.timedelta(hours=20)
        end = timezone.now() + datetime.timedelta(hours=1)
        question_can_not_vote = Question(pub_date=end, end_date=time)
        self.assertIs(question_can_not_vote.can_vote(), False)