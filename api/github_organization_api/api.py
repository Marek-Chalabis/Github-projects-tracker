from typing import Optional

import requests

from allauth.socialaccount.models import (
    SocialAccount,
    SocialToken,
)
from crum import get_current_user

from api.github_organization_api.github_api_urls import (
    URL_GET_COMMIT,
    URL_GET_LIST_ORGANIZATION_REPOSITORIES,
    URL_GET_REPOSITORY,
)
from github_projects_tracker.settings import env


class GithubOrganizationApi:
    """Class for retrieving github data for organization.

    Amount of retrieved data will depend on user credential on Github.
    """

    def __init__(self, organization: Optional[str] = None) -> None:
        self.organization = organization or env('ORGANIZATION')

    @property
    def token(self) -> str:
        """Social token for current user."""
        social_account = SocialAccount.objects.get(user=get_current_user())
        return SocialToken.objects.get(account=social_account).token

    def get_repo(self, repo: str) -> requests.Response:
        url = URL_GET_REPOSITORY.format(owner=self.organization, repo=repo)
        return requests.get(url=url, headers={'Authorization': f'Token {self.token}'})

    def get_organization_repos(self) -> requests.Response:
        url = URL_GET_LIST_ORGANIZATION_REPOSITORIES.format(org=self.organization)
        return requests.get(url=url, headers={'Authorization': f'Token {self.token}'})

    def get_commit(self, repo: str, branch: str) -> requests.Response:
        url = URL_GET_COMMIT.format(owner=self.organization, repo=repo, branch=branch)
        return requests.get(url=url, headers={'Authorization': f'Token {self.token}'})
