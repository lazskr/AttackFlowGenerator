# Generated by Django 4.2.4 on 2023-09-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_annotation_rename_last_changed_report_last_updated_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="annotation",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]
