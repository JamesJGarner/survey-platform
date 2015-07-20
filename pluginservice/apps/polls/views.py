from django.views.generic import ListView, CreateView, DetailView, TemplateView
from .models import Poll, PollAnswer
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from pluginservice.settings.production import CURRENT_SITE_URL
from .forms import CreateForm


class PollHome(TemplateView):
    template_name = 'polls/polls_home.html'


class PollList(ListView):
    model = Poll


class PollDetail(DetailView):
    model = Poll


class PollCreate(CreateView):
    model = Poll
    form_class = CreateForm
    #success_url = '/polls/create/success/'

    def form_valid(self, form):
        PollForm = form.save(commit=False)
        PollForm.created_by = self.request.user
        self.object = form.save()

        choice1 = form.cleaned_data['choice1']
        choice2 = form.cleaned_data['choice2']
        choice3 = form.cleaned_data['choice3']

        
        if choice1 != "":
            CreateAnswers = PollAnswer.objects.create(poll=self.object, answer=choice1)
            CreateAnswers.save()

        if choice2 != "":
            CreateAnswers = PollAnswer.objects.create(poll=self.object, answer=choice2)
            CreateAnswers.save()

        if choice3 != "":
            CreateAnswers = PollAnswer.objects.create(poll=self.object, answer=choice3)
            CreateAnswers.save()


        return super(PollCreate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('polls:success', kwargs={'pk': self.object.id})


class PollCreateSuccess(DetailView):
    model = Poll
    template_name = 'polls/poll_success.html'

    def get_context_data(self, **kwargs):
        context = super(PollCreateSuccess, self).get_context_data(**kwargs)
        context['current_site_url'] = CURRENT_SITE_URL
        return context