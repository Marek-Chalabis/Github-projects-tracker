from crum import get_current_user
from django.db import models


class LowerCaseCharField(models.CharField):

    def get_prep_value(self, field_value: str) -> str:
        """Overwrite this for DRF."""
        return str(field_value).lower()


class Project(models.Model):

    added_by = models.ForeignKey(
        'auth.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_added_by',
    )
    project_name = LowerCaseCharField(max_length=80, unique=True)

    def save(self, *args, **kwargs) -> None:
        """Store user who added project, lower case project_name for save method."""
        if not self.pk:
            self.added_by = get_current_user()  # noqa: WPS601
        self.project_name = self.project_name.lower()  # noqa: WPS601
        super().save(*args, **kwargs)
