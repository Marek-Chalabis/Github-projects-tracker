from typing import ClassVar

from django.db.models import QuerySet
from django.db.models.functions import Lower
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.github_organization_api import GithubOrganizationApi
from api.github_organization_api.urls import get_project_zip_url
from api.models import Project
from api.serializers import ProjectSerializer
from api.utils import dictionary_compress


class ProjectModelViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    base_fields_to_return: ClassVar[set[str]] = {
        'full_name',
        'language',
        'stargazers_count',
        'updated_at',
    }

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_name__iexact'

    @property
    def monitored_projects(self) -> QuerySet:
        """Returns Organization monitored projects in lowercase."""
        return (
            self.get_queryset()
            .annotate(project_name_lower=Lower('project_name'))
            .values_list('project_name_lower', flat=True)
        )

    def _get_filtered_projects(self) -> filter:
        """Returns projects from Github API which organization monitor."""
        organization_projects = GithubOrganizationApi.get_projects().json()
        return filter(
            lambda project: project['name'].lower() in self.monitored_projects,
            organization_projects,
        )

    def list(self, request, *args, **kwargs) -> Response:
        """Returns only monitored projects."""
        projects_to_return = []
        for project in self._get_filtered_projects():
            projects_to_return.append(
                dictionary_compress(
                    dictionary_to_compress=project,
                    keys_to_keep=self.base_fields_to_return,
                )
            )
        return Response(projects_to_return)

    def retrieve(self, request, *args, **kwargs) -> Response:
        """Returns project with additional data about last commit and download link."""
        project_name = self.get_object().project_name
        project_github = GithubOrganizationApi.get_project(
            project_name=project_name
        ).json()
        project_to_return = dictionary_compress(
            dictionary_to_compress=project_github,
            keys_to_keep=self.base_fields_to_return,
        )
        last_commit = GithubOrganizationApi.get_last_commit_on_branch(
            project_name=project_name,
            branch=project_github['default_branch'],
        ).json()
        project_to_return['commit'] = {
            'author': last_commit['commit']['author'],
            'message': last_commit['commit']['message'],
        }
        project_to_return['download_link'] = get_project_zip_url(
            project_name=project_name
        )
        return Response(project_to_return)
