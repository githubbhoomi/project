# Generated by Django 4.2 on 2023-06-07 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0017_alter_studentmark_languages_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="subject",
            name="k",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="app1.studentmark",
            ),
            preserve_default=False,
        ),
    ]
