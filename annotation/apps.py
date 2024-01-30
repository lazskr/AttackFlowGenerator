"""Module defines the application configuration for the 'annotation' app.

This configuration is used by Django to handle application-specific settings
and to integrate the app into the project.
"""

from django.apps import AppConfig


class AnnotationConfig(AppConfig):
    """Configuration class for the 'annotation' app.

    This class inherits from `AppConfig` and defines the default settings for the
    'annotation' app. These settings include the default auto field type and the app's name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "annotation"
