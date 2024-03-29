# Generated by Django 2.0.7 on 2019-04-12 14:29

import cqexam.models
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CqExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=cqexam.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('setname', models.CharField(blank=True, max_length=50)),
                ('items', models.IntegerField(default=0)),
                ('mark', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('qlist', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), size=None)),
                ('privacy', models.CharField(choices=[('o', 'Open'), ('c', 'Closed'), ('p', 'Private')], default='o', max_length=1)),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cqexam_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
    ]
