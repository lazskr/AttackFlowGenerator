# Generated by Django 4.2.4 on 2023-09-01 13:34

from django.db import migrations, models
import django.db.models.deletion
import reports.models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="report",
            name="upload_date",
        ),
        migrations.AddField(
            model_name="report",
            name="last_changed",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="report",
            name="file",
            field=models.FileField(
                upload_to=reports.models.file_upload_path,
                validators=[reports.models.validate_file],
            ),
        ),
        migrations.CreateModel(
            name="Document",
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
                ("upload_date", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.FileField(
                        upload_to=reports.models.file_upload_path,
                        validators=[reports.models.validate_file],
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="reports.report"
                    ),
                ),
            ],
        ),
    ]
