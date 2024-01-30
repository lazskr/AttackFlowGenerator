"""Forms for allowing users to upload annotations."""
from django import forms  # provide skeleton for report form

from .models import Annotation


class AnnotationForm(forms.ModelForm):
    """The form for uploading an annotation."""

    class Meta:
        """Meta class associates this form to a model."""

        model = Annotation
        fields = ["annotation"]
