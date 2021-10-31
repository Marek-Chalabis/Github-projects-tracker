from typing import (
    ClassVar,
    Iterator,
)

from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from api.github_organization_api import GithubOrganizationApi
from api.github_organization_api.github_api_urls import (
    URL_DOWNLOAD_REPOSITORY_ARCHIVE_ZIP,
)
from api.models import Project
from api.serializers import ProjectSerializer
from api.utils_api import dictionary_compress
from github_projects_tracker.settings import env


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
        """Organization monitored projects."""
        return self.get_queryset().values_list('project_name', flat=True)

    def list(self, request, *args, **kwargs) -> Response:
        """Projects monitored by organization available for current user."""
        organization_projects_response = (
            GithubOrganizationApi().get_organization_repos()
        )
        if organization_projects_response.status_code == HTTP_200_OK:
            all_projects = organization_projects_response.json()
            monitored_projects = self._get_monitored_projects(
                organization_projects=all_projects,
            )
            projects_to_return = [
                dictionary_compress(
                    dictionary_to_compress=project,
                    keys_to_keep=self.base_fields_to_return,
                )
                for project in monitored_projects
            ]
            return Response(projects_to_return)
        return Response(
            data={
                'response_from_github': organization_projects_response.json(),
                'github_endpoint': organization_projects_response.url,
            },
            status=organization_projects_response.status_code,
        )

    def retrieve(self, request, *args, **kwargs) -> Response:
        """Project with additional data about last commit and download link."""
        github_api = GithubOrganizationApi()
        project_name = self.get_object().project_name
        project_github_response = github_api.get_repo(repo=project_name)
        if project_github_response.status_code == HTTP_200_OK:
            project = project_github_response.json()
            project_to_return = dictionary_compress(
                dictionary_to_compress=project,
                keys_to_keep=self.base_fields_to_return,
            )
            last_commit = github_api.get_commit(
                repo=project_name,
                branch=project['default_branch'],
            ).json()
            project_to_return['commit'] = {
                'author': last_commit['commit']['author'],
                'message': last_commit['commit']['message'],
            }
            project_to_return[
                'download_link'
            ] = URL_DOWNLOAD_REPOSITORY_ARCHIVE_ZIP.format(
                owner=env('ORGANIZATION'),
                repo=project_name,
            )
            return Response(project_to_return)
        return Response(
            data={
                'response_from_github': project_github_response.json(),
                'github_endpoint': project_github_response.url,
            },
            status=project_github_response.status_code,
        )

    def _get_monitored_projects(
        self,
        organization_projects: list,
    ) -> Iterator:
        """Projects from Github API which organization monitor."""
        return filter(
            lambda project: project['name'].lower() in self.monitored_projects,
            organization_projects,
        )
