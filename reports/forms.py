"""Forms for allowing users to upload reports."""
from django import forms  # provide skeleton for report form

from .models import Report

#  Report form (via forms)
#  The ReportForm is a helper class which will create a form based on the Report model (in models.py)
#  The Meta inner class aids in aiding meta data about the ReportForm class.

# model = Report specifies that the form is based on the Report model. Thus, when creating a form instance, it will
# will be creating a Report instance in the database


class ReportForm(forms.ModelForm):
    """The form for uploading a report."""

    class Meta:  # Meta helps generating forms based on a model (in this case, Report)
        """Meta class associates this form to a model."""

        # model and fields is specific to Meta class and names cannot be changed
        model = Report  # ties form to Report model
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "accept": "application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
            )
        }

        # generated form will hide upload date, represents the variables or fields from Report model
        fields = ["name", "file"]
