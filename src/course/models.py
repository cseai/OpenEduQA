import time
from django.db import models
from django.urls import reverse
from level.models import Level
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class SubjectManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(SubjectManager, self).filter(active=True, draft=False)


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    # SubjectModel = instance.__class__
    # new_id = SubjectModel.objects.order_by("id").last().id + 1
    new_id = 'subject'
    app_name = "course"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Subject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    short_name = models.CharField(max_length=10)
    related_names = ArrayField(models.CharField(max_length=50), blank=True)
    reladed_levels = ArrayField(models.IntegerField(blank=True), blank=True)
    ordering_code = models.IntegerField(default=0)

    BANGLA = 'bn'
    ENGLISH = 'en'
    ARABI = 'ar'
    MEDIUM_CHOICES = (
        (BANGLA, 'Bangla'),
        (ENGLISH, 'English'),
        (ARABI, 'Arabi'),
    )

    medium = models.CharField(
        max_length=3,
        choices=MEDIUM_CHOICES,
        default=BANGLA,
    )

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

    objects = SubjectManager()

    class Meta:
        ordering = ["level", "ordering_code", "code", "name"]

    def __str__(self):
        return f"{self.name} ->({self.level})"

    def get_absolute_url(self):
        return reverse("course:detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("course:update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("course:delete", kwargs={"id": self.id})

    @property
    def get_medium(self):
        for m in self.MEDIUM_CHOICES:
            if m[0] == self.medium:
                return m[1]
        return "Undefined"
