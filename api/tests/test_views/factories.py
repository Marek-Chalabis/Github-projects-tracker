from factory.django import DjangoModelFactory


class ProjectFactory(DjangoModelFactory):
    project_name = 'test_project_name'

    class Meta:
        model = 'api.Project'
