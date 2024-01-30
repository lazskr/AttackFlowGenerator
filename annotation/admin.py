"""Register models with admin panel."""

from django.contrib import admin

from .models import Annotation

# Register your models here.

# will be able to view the annotation objects in the admin dashboard
admin.site.register(Annotation)
