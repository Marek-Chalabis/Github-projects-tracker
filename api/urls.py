from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from api.social_auth import GithubLogin
from api.views import ProjectModelViewSet

router = DefaultRouter()
router.register('projects', ProjectModelViewSet, basename='projects')

urlpatterns = [
    path('v1/', include(router.urls)),
    url('v1/documentation/', get_swagger_view(title='API Endpoints')),
    path('v1/login_github/', GithubLogin.as_view(), name='login_github'),
]