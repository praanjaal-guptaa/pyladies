from django.conf.urls import url

from .views import UpdateProfileView, ProfileView, UpdateLoginView, CreateProfileView, PasswordView


urlpatterns = [
    url(r'profiles/create_profile/$', CreateProfileView.as_view(), name='create_profile'),
    url(r'profiles/update/(?P<pk>\d+)/$', UpdateProfileView.as_view(), name='update'),
    url(r'profiles/home/$', ProfileView.as_view(), name='profile_home'),
    url(r'profiles/login_details/password/$', PasswordView.as_view(), name='password'),
    url(r'profiles/login_details/(?P<pk>\d+)/$', UpdateLoginView.as_view(), name='login_details'),
]
