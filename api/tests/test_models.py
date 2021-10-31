import pytest

from django.contrib.auth.models import User

from api.models import Project


@pytest.mark.django_db()
class TestBaseCycle:
    def test_project_name_lower_case(self):
        project = Project.objects.create(project_name='TEST')
        assert project.project_name == 'test'

    def test_project_added_by(self, mocker):
        test_user = User.objects.create(username='testuser')
        mocker.patch('api.models.get_current_user', return_value=test_user)
        test_project = Project.objects.create(project_name='Test1')
        assert test_project.added_by == test_user
