# Generated by Django 2.0.7 on 2019-04-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0002_level_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
