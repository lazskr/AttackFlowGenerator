# Generated by Django 4.2.4 on 2023-10-17 07:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0007_report_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Annotation",
        ),
    ]
