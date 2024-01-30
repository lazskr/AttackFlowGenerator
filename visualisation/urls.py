"""urls that go to different views in the views.py file."""
from django.urls import path

from . import views

#  url paths for our website (e.g. /upload will take us to upload.html)
urlpatterns = [
    path("", views.index, name="visualise_test"),
    path("<id>", views.visualise_annotation, name="visualise_view"),
]
