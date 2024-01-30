"""urls that go to different views in the views.py file."""
from django.urls import path

from . import views

#  url paths for our website (e.g. / will take us to annotation.html)
urlpatterns = [
    path("edit/<id>", views.annotation_edit, name="annotation_edit"),
    path("view/<id>", views.annotation_view, name="annotation_view"),
]
