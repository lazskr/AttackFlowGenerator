"""urls that go to different views in the views.py file."""
from django.urls import path

from . import views

#  url paths for our website (e.g. /upload will take us to upload.html)
urlpatterns = [
    path("upload/", views.report_upload, name="report_upload"),
    path("update/<id>", views.report_update, name="report_update"),
    path("", views.report_list, name="report_list"),
    path("<id>", views.report_details, name="report_details"),
]
