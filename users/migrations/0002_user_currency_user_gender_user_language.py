# Generated by Django 4.1.5 on 2023-01-11 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.CharField(
                choices=[("won", "Korean Won"), ("usd", "Dollar")],
                default="",
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[("kr", "Korean"), ("en", "English")],
                default="",
                max_length=100,
            ),
        ),
    ]
