# Generated by Django 4.2 on 2023-06-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0010_lecturer_image_alter_studentmark_s1"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="image",
            field=models.ImageField(default=False, upload_to="pics"),
        ),
    ]
