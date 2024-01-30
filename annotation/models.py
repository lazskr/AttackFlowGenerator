"""Models for the annotations."""
from django.db import models

from reports.models import Report


class Annotation(models.Model):
    """Model for the annotations created by users."""

    annotation = models.JSONField()
    upload_date = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report, models.CASCADE)
    verified = models.BooleanField(default=False)
