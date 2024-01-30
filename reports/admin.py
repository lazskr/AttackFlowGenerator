"""Register all of the report models so they are accessible from the admin dashboard."""

from django.contrib import admin

from .models import Report

# Register your models here.
admin.site.register(Report)
