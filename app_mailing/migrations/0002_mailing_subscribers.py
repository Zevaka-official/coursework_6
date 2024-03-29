# Generated by Django 4.2.7 on 2024-02-01 10:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_mailing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailing",
            name="subscribers",
            field=models.ManyToManyField(
                related_name="subscriptions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Получатели",
            ),
        ),
    ]
