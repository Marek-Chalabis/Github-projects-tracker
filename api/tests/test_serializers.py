from unittest.mock import Mock

import pytest

from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from api.serializers import ProjectSerializer


class TestProjectSerializer:
    def test_validate_project_name_correct(self, mocker):
        mocker_response = mocker.patch(
            'api.serializers.GithubOrganizationApi.get_repo',
            Mock,
        )
        mocker_response.status_code = HTTP_200_OK
        assert ProjectSerializer().validate_project_name('test') == 'test'

    def test_validate_project_name_not_exists(self, mocker):
        mocker_response = mocker.patch(
            'api.serializers.GithubOrganizationApi.get_repo',
            Mock,
        )
        mocker_response.status_code = HTTP_404_NOT_FOUND
        mocker_response.url = 'test_url'
        with pytest.raises(
            ValidationError,
            match=(
                "[ErrorDetail(string='Project(test) does not exists(test_url)', "
                + "code='invalid')]"
            ),
        ):
            ProjectSerializer().validate_project_name('test')

    def test_validate_project_name_not_authorize(self, mocker):
        mocker_response = mocker.patch(
            'api.serializers.GithubOrganizationApi.get_repo',
            Mock,
        )
        mocker_response.status_code = HTTP_401_UNAUTHORIZED
        mocker_response.url = 'test_url'
        with pytest.raises(
            ValidationError,
            match=(
                "[ErrorDetail(string='You are not authorized to add "
                + "this Project(test)', code='invalid')]"
            ),
        ):
            ProjectSerializer().validate_project_name('test')
