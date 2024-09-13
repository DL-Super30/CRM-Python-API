# Generated by Django 5.1 on 2024-09-13 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cretebatch", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="createbatches",
            name="location",
            field=models.ForeignKey(
                choices=[("Hyderabad", "Hyderabad")],
                default="Hyderabd",
                on_delete=django.db.models.deletion.CASCADE,
                to="cretebatch.location",
            ),
        ),
    ]
