from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from github_projects_tracker.settings import env


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url: str = env('CALLBACK_URL')
    client_class = OAuth2Client
