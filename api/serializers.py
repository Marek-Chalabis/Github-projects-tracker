from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from api.github_organization_api import GithubOrganizationApi
from api.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('project_name',)

    def validate_project_name(self, project_name) -> str:
        """Checks if project exists for organization and user can add it."""
        project = GithubOrganizationApi.get_project(project_name)
        if project.status_code == HTTP_404_NOT_FOUND:
            raise ValidationError(
                f'Project({project_name}) does not exists({project.url})'
            )
        if project.status_code == HTTP_401_UNAUTHORIZED:
            raise ValidationError(
                f'You are not authorized to add this Project({project_name})'
            )
        return project_name
