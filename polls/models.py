"""import user model timezone"""

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class Question(models.Model):
    """set a question"""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)


    def __str__(self):
        """return str"""
        return self.question_text

    def was_published_recently(self):
        """check is it public"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """if pubtime is not over yet,return True"""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """if voting is currently allowed for this question,return true """
        now = timezone.now()
        return (self.pub_date <= now) and (self.end_date is None or now <= self.end_date)


class Choice(models.Model):
    """set a choice"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    @property
    def vote(self):
        count = Votes.objects.filter(choice=self).count()
        return count


class Votes(models.Model):
    """Class Vote"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        """Return string."""
        return f"Vote by {self.user.user_name} for {self.choice.choice_text}"

    @property
    def question(self):
        """Get question."""
        return self.choice.question
