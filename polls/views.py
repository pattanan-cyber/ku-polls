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
        return Question.objects.filter(pub_date__lte=timezone.now()) \
                   .order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    """detail view"""
    model = Question
    template_name = 'polls/detail.html'


    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, **kwargs):
        """If question doesn't exist/can't be vote, redirect to index page."""
        try:
            self.object = self.get_object()
            return self.render_to_response(self.get_context_data
            (object=self.get_object))
        except:
            messages.error(request, "This poll is unavailable.")
            return HttpResponseRedirect(reverse('polls:index'))

class ResultsView(generic.DetailView):
    """result view"""
    model = Question
    template_name = 'polls/results.html'

def index(request):
    """index"""
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    """detail"""
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    """"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
