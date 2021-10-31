import pytest

from django.urls import reverse
from rest_framework.status import HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'url_name',
    [
        'documentation',
        'login_github',
    ],
)
def test_api_urls(client, url_name):
    response = client.get(reverse(url_name))
    assert response.status_code != HTTP_404_NOT_FOUND
