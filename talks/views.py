from django.http import HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
from talks.models import (Suggestion, Proposal)
from talks.forms import ProposalForm, SuggestForm
from .mixins import LoginRequiredMixin

from pyladies_harare.views import get_meetup, get_category


class CreateTalkView(LoginRequiredMixin, CreateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "talks/talk_form.html"

    def get_context_data(self, **kwargs):
        context = super(CreateTalkView, self).get_context_data(**kwargs)
        context['title'] = 'Submit A Talk'
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateTalkView, self).get_form_kwargs()
        return kwargs

    def get_form_valid_message(self):
        msg = ugettext('Talk proposal <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)
    

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        
        # Save the author information as well (many-to-many fun)
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class TalkView(DetailView):
    model = Proposal
    template_name = "talks/talk.html"

    def get_object(self,*args, **kwargs):
        object = super(TalkView, self).get_object(*args, **kwargs)
        return object

    def get_contex_data(self, **kwargs):
        context = super(TalkView, self).get_contex_data(**kwargs)
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['title'] = 'View Talk'
        return context


class TalkListView(ListView):
    model = Proposal
    template_name = "talks/talk_list.html"

    def get_context_data(self, **kwargs):
        context = super(TalkListView, self).get_contex_data(**kwargs)
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['title'] = 'List of Talks'
        return context


class CreateSuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    form_class = SuggestForm
    template_name = "talks/suggest_form.html"

    def get_context_data(self, **kwargs):
        context = super(CreateSuggestionView, self).get_context_data(**kwargs)
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['title'] = 'Suggest a Talk'
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateSuggestionView, self).get_form_kwargs()
        return kwargs

    def get_form_valid_message(self):
        msg = ugettext('Talk suggestion <strong>{title}</strong> created.')
        return format_html(msg, title=self.object.title)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        # Save the author information as well (many-to-many fun)
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class SuggestionView(DetailView):
    model = Suggestion
    template_name = "talks/suggestions.html"

    def get_context_data(self, **kwargs):
        context = super(SuggestionView, self).get_context_data(**kwargs)
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['title'] = 'View Suggested Talk'
        return context

    def get_object(self, *args, **kwargs):
        obj = super(SuggestionView, self).get_object(*args, **kwargs)
        return obj




class SuggestionListView(ListView):
    model = Suggestion
    template_name = "talks/suggestion_list.html"

    def get_context_data(self, **kwargs):
        context = super(SuggestionListView, self).get_contex_data(**kwargs)
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['title'] = 'View Suggested Talk'
        return context

