"""requests to the polls"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


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


def vote(request, question_id):
    """vote the poll"""

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
