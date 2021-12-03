"""Views handle requests to the polls app."""
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Votes
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    """Index class."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now())\
            .order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail class."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, **kwargs):
        """If question doesn't exist/can't be vote, redirect to index page."""
        try:
            self.object = self.get_object()
            return self.render_to_response(self.get_context_data(
                object=self.get_object))
        except:
            messages.error(request, "This poll is unavailable.")
            return HttpResponseRedirect(reverse('polls:index'))


class ResultsView(generic.DetailView):
    """Result class."""

    model = Question
    template_name = 'polls/results.html'

@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Vote for each question by using question_id."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "This poll is unavailable.")
        return HttpResponseRedirect(reverse('polls:index'))
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't selected a choice.",
        })
    else:
        # Record the vote
        user = request.user
        # get the previous vote for this user(may not have)
        vote = get_vote_for_user(user, question)
        # Case 1 user has not voted for this poll question yet
        #        Create a new vote object
        if not vote:
            vote = Votes.objects.create(user=user, choice=selected_choice)
        else:
            # Case 2: user has already voted
            # Modify the existing vote and save it
            vote.choice = selected_choice
        vote.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))

def logged_out(request):
    """Log out."""
    return redirect('logout')

def get_vote_for_user(user, poll_question):
    """Find and return an existing vote for a user on a poll question.
    Returns:
        The user's Vote or None if no vote fot this pol_question
    """
    try:
        votes = Votes.objects.filter(user=user).filter(choice__question=poll_question)
        # should be at most one Vote
        if votes.count() == 0:
            return None
        return votes[0]
    except Votes.DoesNotExist:
        return []

def signup(request):
    """Create new user."""
    if request.method == 'POST':
        User.objects.create_user(
            request.POST['username'],
            request.POST["email"],
            request.POST["password"]
        )
        # success fully create new user and redirect
        return redirect('login')
    return render(request, 'registration/sign_up.html')



