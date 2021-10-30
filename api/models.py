from django.db import models

from allauth.socialaccount.models import SocialAccount, SocialToken
from crum import get_current_user


class Project(models.Model):

    added_by = models.ForeignKey(
        'auth.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_added_by',
    )
    project_name = models.CharField(max_length=80, unique=True)

    def save(self, *args, **kwargs):
        """Store user who added project to monitor"""
        if not self.pk:
            self.added_by = get_current_user()
        super().save(*args, **kwargs)
