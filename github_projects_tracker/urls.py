from django.contrib import admin
from django.urls import path

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/github/login/callback/'
    client_class = OAuth2Client

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/github/', GithubLogin.as_view(), name='github_login'),
]
