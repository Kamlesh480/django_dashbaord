# Generated by Django 4.2 on 2023-04-25 03:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_setting", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="automationcredentials",
            name="username",
        ),
    ]