# Generated by Django 4.1.5 on 2023-01-11 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Perk",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("detail", models.CharField(max_length=50)),
                ("explanation", models.TextField()),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Experience",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=250)),
                ("country", models.CharField(default="대한민국", max_length=50)),
                ("city", models.CharField(default="경주", max_length=80)),
                ("price", models.PositiveIntegerField()),
                ("address", models.CharField(max_length=250)),
                ("start", models.TimeField()),
                ("end", models.TimeField()),
                ("descriptions", models.TextField(max_length=500)),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("perk", models.ManyToManyField(to="experiences.perk")),
            ],
            options={"abstract": False,},
        ),
    ]