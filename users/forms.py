"""Forms for user-related data."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#  Report form (via forms)
#  The ReportForm is a helper class which will create a form based on the Report model (in models.py)
#  The Meta inner class aids in aiding meta data about the ReportForm class.

# model = Report specifies that the form is based on the Report model. Thus, when creating a form instance, it will
# will be creating a Report instance in the database


class NewUserForm(UserCreationForm):
    """Form for user data."""

    class Meta:
        """Meta Class."""

        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """Save the form to the database."""
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
