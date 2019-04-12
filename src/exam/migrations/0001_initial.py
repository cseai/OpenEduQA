# Generated by Django 2.0.7 on 2019-04-12 14:29

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import exam.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=exam.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('subjects', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('setname', models.CharField(blank=True, max_length=50)),
                ('items', models.IntegerField(default=0)),
                ('mark', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('hascq', models.BooleanField(default=False)),
                ('hasmcq', models.BooleanField(default=False)),
                ('cqelist', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, size=None)),
                ('mcqelist', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), blank=True, size=None)),
                ('privacy', models.CharField(choices=[('o', 'Open'), ('c', 'Closed'), ('p', 'Private')], default='o', max_length=1)),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
    ]