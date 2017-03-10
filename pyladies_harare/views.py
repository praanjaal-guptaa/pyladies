from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponseRedirect

from datetime import datetime
from .models import Post, Meetup, Page, Contact, Category
from .forms import ContactForm, CommentForm


def get_meetup():
    meetups = Meetup.objects.filter(ispast=False).order_by('fromdate')
    return meetups

def get_past_meetup():
    past_meetups = Meetup.objects.filter(ispast=True).order_by('-fromdate')
    return past_meetups

def get_category():
    categories = Category.objects.all()
    return categories


def home(request):
    assert isinstance(request, HttpRequest)
    post_list = Post.objects.all().order_by('-published_date')
    categories = get_category()
    meetups = get_meetup()

    paginator = Paginator(post_list, 3)  # Show 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'pyladies_harare/index.html',
        {
            'title': 'Home Page',
            'message': 'Home Page.',
            'year': datetime.now().year,
            'meetups': meetups,
            'posts': posts,
            'categories': categories,
        }
    )


def past_meetups(request):
    """Renders past meet-ups"""
    assert isinstance(request, HttpRequest)
    upcoming = get_meetup()
    meetup_list = get_past_meetup()

    paginator = Paginator(meetup_list, 2)  # Show 2 meet-ups per page
    page = request.GET.get('page')
    try:
        p_meetups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        p_meetups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        p_meetups = paginator.page(paginator.num_pages)
    return render(
            request,
            'pyladies_harare/past.html',
             {
                'title': 'Past Meetups',
                'message': 'Past Meetups.',
                'year': datetime.now().year,
                'p_meetups': p_meetups,
                'upcoming': upcoming,
            }
            )


class AboutView(TemplateView):
    template_name = "pyladies_harare/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['title'] = 'About'
        context['pages'] = Page.objects.filter(slug='about')
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class MeetupsView(TemplateView):
    template_name = "pyladies_harare/meetups.html"

    def get_context_data(self, **kwargs):
        context = super(MeetupsView, self).get_context_data(**kwargs)
        context['title'] = 'Our Meetups'
        context['pages'] = Page.objects.filter(slug='meetups')
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class UpcomingView(TemplateView):
    template_name = "pyladies_harare/upcoming.html"

    def get_context_data(self, **kwargs):
        context = super(UpcomingView, self).get_context_data(**kwargs)
        context['title'] = 'Upcoming Meetups'
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class PostDetailView(TemplateView):
    template_name = "pyladies_harare/post_detail.html"
    comment_form = CommentForm()

    def get_context_data(self, pk, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Blog Post'
        context['categories'] = get_category()
        context['post'] = get_object_or_404(Post, pk=pk)
        context['meetups'] = get_meetup()
        context['comment_form'] = self.comment_form
        context['year'] = datetime.now().year
        return context


class ContactView(TemplateView):
    template_name = "pyladies_harare/contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        contact_form = ContactForm()
        context['contact_form'] = contact_form
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context

    def post(self, request):
        contact_form = ContactForm(request.POST)
        contact_form.save()

        to = ['harare@pyladies.com']
        subject = request.POST.get('subject', '')
        details = request.POST.get('message', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone')
        name = request.POST.get('name')

        if contact_form.is_valid():
                # process the data in feedback_form.cleaned_data as required
                obj = Contact()  # gets new object
                obj.name = contact_form.cleaned_data['name']
                obj.phone = contact_form.cleaned_data['phone']
                obj.email = contact_form.cleaned_data['email']
                obj.subject = contact_form.cleaned_data['subject']
                obj.message = contact_form.cleaned_data['message']
                # finally save the object in db
                obj.save()

                # send email to infoharare@genaulabs.com
                subject = "Message on Contact Form - " + contact_form.cleaned_data['subject']
                message = 'A message was submitted on the website\n\n'
                message += 'Name: ' + contact_form.cleaned_data['name'] + '\n'
                message += 'Email: ' + contact_form.cleaned_data['email'] + '\n'
                message += 'Phone: ' + contact_form.cleaned_data['phone'] + '\n'
                message += 'Message:\n ' + contact_form.cleaned_data['message'] + '\n'

                sender = 'harare@pyldies.com'

                recipient_list = ['harare@pyladies.com']
                send_mail(subject, message, sender, recipient_list)

                # redirect to a new URL:
                return HttpResponseRedirect('/thanks/')


class CodeofConductView(TemplateView):
    template_name = "pyladies_harare/code_of_conduct.html"

    def get_context_data(self, **kwargs):
        context = super(CodeofConductView, self).get_context_data(**kwargs)
        context['title'] = 'Code of Conduct'
        context['pages'] = Page.objects.filter(slug='code_of_conduct')
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class TalkTypesView(TemplateView):
    template_name = "pyladies_harare/talk_types.html"

    def get_context_data(self, **kwargs):
        context = super(TalkTypesView, self).get_context_data(**kwargs)
        context['title'] = 'Talk Types'
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class TopicsView(TemplateView):
    template_name = "pyladies_harare/topics.html"

    def get_context_data(self, **kwargs):
        context = super(TopicsView, self).get_context_data(**kwargs)
        context['title'] = 'Topics of Interest'
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


class ThanksView(TemplateView):
    template_name = "pyladies_harare/thanks.html"

    def get_context_data(self, **kwargs):
        context = super(ThanksView, self).get_context_data(**kwargs)
        context['title'] = 'Thank you'
        context['categories'] = get_category()
        context['meetups'] = get_meetup()
        context['year'] = datetime.now().year
        return context


def search(request):
    query = request.GET['q']
    t = loader.get_template('template/results.html')
    c = Context({ 'query': query,})
    return HttpResponse(t.render(c))
