import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class PollDatesTests(TestCase):
    """Tests of question model."""

    def setUp(self):
        """Create constant itme use for tests in this class."""
        self.add_time_one_year = datetime.timedelta(days=365)

    def test_was_published_recently_with_future_question(self):
        """Test for was_published_recently().
        was_published_recently() must returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        end_time = time+self.add_time_one_year
        future_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test for was_published_recently().
        was_published_recently() must returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        end_time = time+self.add_time_one_year
        old_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test for was_published_recently().
        was_published_recently() must returns True for questions whose pub_date is within the last day.
        """
        delta = datetime.timedelta(hours=23, minutes=59, seconds=59)
        time = timezone.now() - delta
        end_time = time+self.add_time_one_year
        recent_question = Question(pub_date=time, end_date=end_time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_publish_the_time_is_publish(self):
        """the time is on time.It should return True."""
        time1 = timezone.now()
        time2 = timezone.now() + datetime.timedelta(minutes=20)
        question_publish1 = Question(pub_date=time1)
        self.assertIs(question_publish1.is_published(), True)
        question_publish2 = Question(pub_date=time2)
        self.assertIs(question_publish2.is_published(), True)

    def test_can_vote_with_current_question(self):
        """The question is publish if it still on time.It should return True."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end1 = timezone.now() + datetime.timedelta(hours=2)
        end2 = timezone.now() + datetime.timedelta(seconds=15)
        question_publish1 = Question(pub_date=time, end_date=end1)
        self.assertIs(question_publish1.is_published(), True)
        question_publish2 = Question(pub_date=time, end_date=end2)
        self.assertIs(question_publish2.is_published(), True)

    def test_this_question_is_can_vote(self):
        """The question can vote if it still on time.It should return True."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        end = timezone.now() + datetime.timedelta(hours=2)
        time1 = timezone.now() - datetime.timedelta(minutes=50)
        end1 = timezone.now() + datetime.timedelta(hours=10)
        question_can_vote1 = Question(pub_date=end, end_date=time)
        self.assertIs(question_can_vote1.can_vote(), True)
        question_can_vote2 = Question(pub_date=end1, end_date=time1)
        self.assertIs(question_can_vote2.can_vote(), True)

    def test_this_question_is_can_not_vote(self):
        """The question can not vote if it still on time.It should return True."""
        time = timezone.now() + datetime.timedelta(hours=20)
        end = timezone.now() + datetime.timedelta(hours=1)
        question_can_not_vote = Question(pub_date=end, end_date=time)
        self.assertIs(question_can_not_vote.can_vote(), False)