import time
from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
# from django.db.models.signals import pre_save, post_save
# from notifications.signals import notify
# from django.dispatch import receiver

# from django.utils import timezone
# from django.utils.safestring import mark_safe
# from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


class LevelManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(LevelManager, self).filter(active=True, draft=False)


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    # LevelModel = instance.__class__
    # new_id = LevelModel.objects.order_by("id").last().id + 1
    new_id = 'level'
    app_name = "level"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Level(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    short_name = models.CharField(max_length=10)
    related_names = ArrayField(models.CharField(max_length=50), blank=True)
    ordering_code = models.IntegerField(default=0)
    description = models.TextField()
    tags = ArrayField(models.CharField(max_length=50), blank=True)

    image = models.ImageField(
        default='default.jpg',
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    draft = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    # initial_year =
    # finished_year =
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = LevelManager()

    def __str__(self):
        return f"{self.name} [{self.short_name}]"

    def get_absolute_url(self):
        return reverse("level:detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("level:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("level:delete", kwargs={"id": self.id})

    class Meta:
        ordering = ["ordering_code", "code", "name"]
