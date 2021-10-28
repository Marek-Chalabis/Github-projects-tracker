from django.contrib import admin
from django.urls import path, include

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
