# Generated by Django 4.1.5 on 2024-02-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eventcalendar", "0003_lessonrequest_lesson_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="events",
            name="requested_by_user_id",
            field=models.CharField(max_length=30),
        ),
    ]
