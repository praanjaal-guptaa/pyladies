from django.conf.urls import url
from talks.views import (CreateTalkView, TalkView, CreateSuggestionView, SuggestionView)

urlpatterns = [
    url(r'submit_talk', CreateTalkView.as_view(), name='create_talks'),
    url(r'^(?P<pk>\d+)/$', TalkView.as_view(), name='pyladies_talk'),
    url(r'suggest_talk', CreateSuggestionView.as_view(), name='suggest_talk'),
    url(r'^(?P<pk>\d+)/$', SuggestionView.as_view(), name='suggested_talk'),
    ]

