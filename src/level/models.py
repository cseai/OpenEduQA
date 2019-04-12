import time
from django.db import models
from django.contrib.postgres.fields import ArrayField


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    LevelModel = instance.__class__
    new_id = LevelModel.objects.order_by("id").last().id + 1
    app_name = "level"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Level(models.Model):
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

    active = models.BooleanField(default=True)
    # initial_year =
    # finished_year =
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["ordering_code", "code", "name"]
