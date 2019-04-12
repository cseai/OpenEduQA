from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from course.models import Subject
# Create your models here.


class TeacherManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(TeacherManager, self).filter(active=True)


def cv_upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    app_name = "teacher"
    field_name = 'cv'
    return '{0}/{1}/{2}/{3}'.format(app_name, instance.user.id, field_name, new_filename)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    since = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    current_workplaces = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True,
    )
    past_workplaces = ArrayField(
        models.CharField(max_length=255, blank=True),
        null=True,
        blank=True,
    )
    # working_hours = # need to add
    # is_onnet

    courses = models.ManyToManyField(Subject, blank=True)

    cv_file = models.FileField(upload_to=cv_upload_location, null=True, blank=True)
    seeking_job = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = TeacherManager()

    def __str__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse("teacher:teacher", kwargs={'id': self.id})

    def get_profile_update_url(self):
        return reverse("teacher:update")

    @property
    def is_active(self):
        # "Is the teacher active?"
        return self.active

    @property
    def is_seeking_job(self):
        return self.seeking_job
