# Generated by Django 4.2 on 2023-05-17 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0008_alter_subject_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentmark",
            name="s1",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
