from unittest.mock import PropertyMock

from api.github_organization_api import GithubOrganizationApi
from api.github_organization_api.github_api_urls import (
    URL_GET_COMMIT,
    URL_GET_LIST_ORGANIZATION_REPOSITORIES,
    URL_GET_REPOSITORY,
)


class TestGithubOrganizationApi:
    def test_get_repo(self, monkeypatch, mocker):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='test_token',
        )
        requests_mock = mocker.patch('api.github_organization_api.api.requests.get')
        tested_repo_name = 'test_repo'
        tested_organization = 'Test_organization'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        GithubOrganizationApi().get_repo(repo=tested_repo_name)
        requests_mock.assert_called_once_with(
            url=URL_GET_REPOSITORY.format(
                owner=tested_organization,
                repo=tested_repo_name,
            ),
            headers={'Authorization': 'Token test_token'},
        )

    def test_get_organization_repos(self, monkeypatch, mocker):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='test_token',
        )
        requests_mock = mocker.patch('api.github_organization_api.api.requests.get')
        tested_organization = 'Test_organization'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        GithubOrganizationApi().get_organization_repos()
        requests_mock.assert_called_once_with(
            url=URL_GET_LIST_ORGANIZATION_REPOSITORIES.format(org=tested_organization),
            headers={'Authorization': 'Token test_token'},
        )

    def test_get_commit(self, monkeypatch, mocker):
        mocker.patch(
            'api.views.GithubOrganizationApi.token',
            new_callable=PropertyMock,
            return_value='test_token',
        )
        requests_mock = mocker.patch('api.github_organization_api.api.requests.get')
        tested_repo_name = 'test_repo'
        tested_organization = 'Test_organization'
        tested_branch = 'branch_test'
        monkeypatch.setenv('ORGANIZATION', tested_organization)
        GithubOrganizationApi().get_commit(repo=tested_repo_name, branch=tested_branch)
        requests_mock.assert_called_once_with(
            url=URL_GET_COMMIT.format(
                owner=tested_organization,
                repo=tested_repo_name,
                branch=tested_branch,
            ),
            headers={'Authorization': 'Token test_token'},
        )
