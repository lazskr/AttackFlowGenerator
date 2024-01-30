# Generated by Django 4.2.4 on 2023-09-03 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("reports", "0004_annotation_verified"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnnotationX",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unique_id", models.CharField(max_length=255, unique=True)),
                ("start", models.PositiveIntegerField()),
                ("end", models.PositiveIntegerField()),
                ("quote", models.TextField()),
                ("note", models.TextField()),
                ("tags", models.JSONField(blank=True, null=True)),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="reports.report"
                    ),
                ),
            ],
        ),
    ]