from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        questions_with_question_marks = []
        for q in Question.objects.all():
            if q.ends_with_question_mark():
                questions_with_question_marks.append(q)
        return questions_with_question_marks


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
    latest_question_list = Question.objects.all()
    template = loader.get_template('polls/index.html')
    context = {
        'question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)


def detail(request, q_id):
    try:
        question = Question.objects.get(id=q_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    #Shorter way:
    # question = get_object_or_404(Question, id=q_id)
    #get_list_or_404 also exists
    return render(request, "polls/detail.html", {'question': question})


def results(request, q_id):
    question = get_object_or_404(Question, pk=q_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, q_id):
    question = get_object_or_404(Question, id=q_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST['choice']
        )
    except (KeyError, Choice.DoesNotExist):
        #KeyError is while POST['choice'] doesnt exists
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't selected a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#reverse() is creating url by reversing job of urls.py
