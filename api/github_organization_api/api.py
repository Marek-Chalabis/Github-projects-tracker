from allauth.socialaccount.models import SocialToken, SocialAccount
from crum import get_current_user

from requests import Response

from api.github_organization_api.github_api_urls import (
    URL_GET_REPOSITORY,
    URL_GET_LIST_ORGANIZATION_REPOSITORIES,
    URL_GET_COMMIT,
)
from github_projects_tracker.settings import env


import requests


class GithubOrganizationApi:
    """Class for retrieving github data for organization.

    Amount of retrieved data will depend on user credential on Github.
    """

    def __init__(self, organization: str = env("ORGANIZATION")) -> None:
        self.organization = organization

    @property
    def token(self) -> str:
        """Returns github token for current user."""
        social_account = SocialAccount.objects.get(user=get_current_user())
        return SocialToken.objects.get(account=social_account).token

    def get_repo(self, repo: str) -> Response:
        url = URL_GET_REPOSITORY.format(owner=self.organization, repo=repo)
        return requests.get(url, headers={'Authorization': f'Token {self.token}'})

    def get_organization_repos(self) -> Response:
        # url = f'{env("GITHUB_API_URL")}/orgs/{env("ORGANIZATION")}/repos' # poprawne
        url = URL_GET_LIST_ORGANIZATION_REPOSITORIES.format(org=self.organization)
        return requests.get(url, headers={'Authorization': f'Token {self.token}'})

    def get_commit(self, repo: str, branch: str) -> Response:
        url = URL_GET_COMMIT.format(owner=self.organization, repo=repo, branch=branch)
        return requests.get(url, headers={'Authorization': f'Token {self.token}'})
