from django.conf.urls import url
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from github_projects_tracker.settings import env

router = DefaultRouter()
# router.register('dishes', DishModelViewSet, basename='dishes')
# router.register('menus', MenuModelViewSet, basename='menus')


from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url: str = env('CALLBACK_URL')
    client_class = OAuth2Client

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token-auth/', views.obtain_auth_token),
    path('v1/register/', GithubLogin.as_view(), name='github_login'),
    url('v1/documentation/', get_swagger_view(title='Pastebin API')), # TODO
]