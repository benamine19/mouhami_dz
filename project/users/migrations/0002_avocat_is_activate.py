# Generated by Django 5.0 on 2023-12-23 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='avocat',
            name='is_activate',
            field=models.BooleanField(default=False),
        ),
    ]