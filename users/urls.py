"""urls that go to different views in the views.py file."""
from django.urls import path

from . import views

#  url paths for our website (e.g. /upload will take us to upload.html)
urlpatterns = [
    path("registration/", views.register_request, name="user_register"),
    path("login/", views.login_request, name="user_login"),
    path("logout/", views.logout_request, name="user_logout"),
]
