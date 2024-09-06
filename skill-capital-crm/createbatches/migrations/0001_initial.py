# Generated by Django 5.1 on 2024-09-06 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Batch",
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
                ("date", models.DateField()),
                ("topic", models.CharField(max_length=200)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("attendance", models.IntegerField(default=0)),
                ("video_upload", models.BooleanField(default=False)),
                ("duration", models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Stack",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CreateBatches",
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
                ("name", models.CharField(max_length=100)),
                ("slot", models.CharField(max_length=100)),
                ("trainer", models.CharField(max_length=100)),
                ("timing", models.CharField(max_length=100)),
                ("class_mode", models.CharField(max_length=100)),
                ("stage", models.CharField(max_length=100)),
                ("comment", models.CharField(max_length=100)),
                ("learners", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("batch_status", models.CharField(max_length=50)),
                ("topic_status", models.CharField(max_length=50)),
                ("no_of_students", models.IntegerField()),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="createbatches.location",
                    ),
                ),
                (
                    "stack",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="createbatches.stack",
                    ),
                ),
            ],
        ),
    ]
