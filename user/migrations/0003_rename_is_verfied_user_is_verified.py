# Generated by Django 5.1 on 2024-08-16 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_user_is_verfied"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_verfied",
            new_name="is_verified",
        ),
    ]
