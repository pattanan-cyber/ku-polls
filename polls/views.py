"""requests to the polls"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """index view"""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """detail view"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, **kwargs):
        """If question doesn't exist/can't be vote, redirect to index page."""
        self.object = self.get_object()
        if self.object.can_vote():
            return self.render_to_response(self.get_context_data(
                object=self.get_object))
        else:
            messages.error(request, "This poll is unavailable.")
            return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """result view"""
    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Make choice be able to vote."""
    user = request.user
    # run this get_object_or_404 if fail return 404 page
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        vote = get_vote_for_user(question, user)
        # Always return an HttpResponseRedirect after successfully dealing
        if not vote:
            vote = Vote(user=user, choice=selected_choice)
        else:
            vote.choice = selected_choice
        vote.save()
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_vote_for_user(question, user):
    try:
        votes = Vote.objects.filter(user=user).filter(choice__question=question)
        if votes.count() == 0:
            return None
        else:
            return votes[0]
    except Vote.DoesNotExist:
        return None