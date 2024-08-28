# Generated by Django 5.1 on 2024-08-27 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Collaborator",
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
                (
                    "access_type",
                    models.CharField(
                        choices=[
                            ("read_only", "Read Only"),
                            ("read_write", "Read and Write"),
                        ],
                        default="read_only",
                        max_length=20,
                    ),
                ),
                (
                    "note",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="collaborators_set",
                        to="notes.note",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "note")},
            },
        ),
        migrations.AddField(
            model_name="note",
            name="collaborator",
            field=models.ManyToManyField(
                related_name="collaborator_note_set",
                through="notes.Collaborator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
