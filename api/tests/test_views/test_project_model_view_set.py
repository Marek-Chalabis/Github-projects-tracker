from unittest.mock import (
    Mock,
    PropertyMock,
)

import pytest
import responses

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from api.github_organization_api.github_api_urls import (
    URL_DOWNLOAD_REPOSITORY_ARCHIVE_ZIP,
    URL_GET_COMMIT,
    URL_GET_LIST_ORGANIZATION_REPOSITORIES,
    URL_GET_REPOSITORY,
)
from api.views import ProjectModelViewSet


@pytest.mark.django_db()
class TestProjectModelViewSet:
    def test_base_fields_to_return(self):
        assert ProjectModelViewSet.base_fields_to_return == {
            'full_name',
            'language',
            'stargazers_count',
            'updated_at',
        }

    def test_monitored_projects(self, project_factory):
        project_factory(project_name='test1')
        project_factory(project_name='TEST2')
        assert list(ProjectModelViewSet().monitored_projects) == ['test1', 'test2']

    def test_get_monitored_projects(self, mocker):
        mocker.patch(
            'api.views.ProjectModelViewSet.monitored_projects',
            new_callable=PropertyMock,
            return_value=['test1', 'test2', 'test3'],
        )
        monitored_projects_test = ProjectModelViewSet()._get_monitored_projects(
            organization_projects=[
                {'name': 'test1'},
                {'name': 'test2'},
                {'name': 'TeSt3'},
                {'name': 'test4'},
            ],
        )
        assert list(monitored_projects_test) == [
            {'name': 'test1'},
            {'name': 'test2'},
            {'name': 'TeSt3'},
        ]

    def test_create_correct(self, client, django_user_model, mocker):
        project_name_test = 'TeSt'
        mocker.patch(
            'api.serializers.ProjectSerializer.validate_project_name',
            return_value=project_name_test,
        )
        user = django_user_model.objects.create(
            username='username',
            password='password',
        )
        client.force_login(user)
        response = client.post('/api/v1/projects/', {'project_name': project_name_test})
        assert response.status_code == HTTP_201_CREATED
        assert response.json() == {'project_name': project_name_test}

    def test_create_un_authorization_access(self, client):
        response = client.post('/api/v1/projects/', {'project_name': 'test'})
        assert response.status_code == HTTP_403_FORBIDDEN

    @responses.activate
    def test_list_not_200(
        self,
        client,
        mocker,
        django_user_model,
        monkeypatch,
    ):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='123',
        )
        user = django_user_model.objects.create(
            username='username',
            password='password',
        )
        client.force_login(user)
        tested_organization = 'Test_organization'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        github_url = URL_GET_LIST_ORGANIZATION_REPOSITORIES.format(
            org=tested_organization,
        )
        responses.add(
            responses.GET,
            github_url,
            json={'tested_data': 1},
            status=HTTP_404_NOT_FOUND,
        )
        response = client.get('/api/v1/projects/')
        assert response.data == {
            'response_from_github': {'tested_data': 1},
            'github_endpoint': github_url,
        }
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_list_correct(
        self,
        client,
        mocker,
        django_user_model,
    ):
        mocker_response = mocker.patch(
            'api.views.GithubOrganizationApi.get_organization_repos',
            Mock,
        )
        mocker_response.status_code = HTTP_200_OK
        mocker.patch(
            'api.views.ProjectModelViewSet._get_monitored_projects',
            return_value=[1, 2, 3],
        )
        mocker.patch('api.views.dictionary_compress', return_value='test')
        user = django_user_model.objects.create(
            username='username',
            password='password',
        )
        client.force_login(user)
        response = client.get('/api/v1/projects/')
        assert response.status_code == HTTP_200_OK
        assert response.data == ['test', 'test', 'test']

    def test_list_un_authorization_access(self, client):
        response = client.get('/api/v1/projects/')
        assert response.status_code == HTTP_403_FORBIDDEN

    @responses.activate
    def test_retrieve_not_200(  # noqa: WPS211
        self,
        client,
        project_factory,
        mocker,
        django_user_model,
        monkeypatch,
    ):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='123',
        )
        user = django_user_model.objects.create(
            username='username',
            password='password',
        )
        client.force_login(user)
        tested_organization = 'Test_organization'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        project_name = 'test1'
        project_factory(project_name=project_name)
        github_url = URL_GET_REPOSITORY.format(
            owner=tested_organization,
            repo=project_name,
        )
        responses.add(
            responses.GET,
            github_url,
            json={'tested_data': 1},
            status=HTTP_404_NOT_FOUND,
        )
        response = client.get(f'/api/v1/projects/{project_name}/')
        assert response.data == {
            'response_from_github': {'tested_data': 1},
            'github_endpoint': github_url,
        }
        assert response.status_code == HTTP_404_NOT_FOUND

    @responses.activate
    def test_retrieve_correct(  # noqa: WPS211
        self,
        client,
        project_factory,
        mocker,
        django_user_model,
        monkeypatch,
    ):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='123',
        )
        mocker.patch(
            'api.views.dictionary_compress',
            return_value={'test_compress': 'test_compress'},
        )
        user = django_user_model.objects.create(
            username='username',
            password='password',
        )
        client.force_login(user)
        tested_organization = 'Test_organization'
        tested_branch = 'test_branch'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        project_name = 'test1'
        github_project_url = URL_GET_REPOSITORY.format(
            owner=tested_organization,
            repo=project_name,
        )
        github_commit_url = URL_GET_COMMIT.format(
            owner=tested_organization,
            repo=project_name,
            branch=tested_branch,
        )
        github_download_url = URL_DOWNLOAD_REPOSITORY_ARCHIVE_ZIP.format(
            owner=tested_organization,
            repo=project_name,
        )
        project_factory(project_name=project_name)
        responses.add(
            responses.GET,
            github_project_url,
            json={'default_branch': 'test_branch'},
            status=HTTP_200_OK,
        )
        responses.add(
            responses.GET,
            github_commit_url,
            json={'commit': {'author': 'test_author', 'message': 'test_message'}},
            status=HTTP_200_OK,
        )
        response = client.get(f'/api/v1/projects/{project_name}/')
        assert response.data == {
            'test_compress': 'test_compress',
            'commit': {'author': 'test_author', 'message': 'test_message'},
            'download_link': github_download_url,
        }
        assert response.status_code == HTTP_200_OK

    def test_retrieve_un_authorization_access(self, client, project_factory):
        project_name = 'test1'
        project_factory(project_name=project_name)
        response = client.get(f'/api/v1/projects/{project_name}/')
        assert response.status_code == HTTP_403_FORBIDDEN
