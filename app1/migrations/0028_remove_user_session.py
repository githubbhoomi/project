# Generated by Django 4.2 on 2023-06-29 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0027_user_session"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="session",
        ),
    ]
