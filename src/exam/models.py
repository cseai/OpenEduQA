import time
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.urls import reverse


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    ExamModel = instance.__class__
    new_id = ExamModel.objects.order_by("id").last().id + 1
    app_name = "exam"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Exam(models.Model):
    '''[summary]
        It is exam of MCQ and/or CQ
    [description]
        List of MCQ and/or CQ will be there and the exam rule
    Extends:
        models.Model
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='exam_user', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    # levels = ArrayField(models.CharField(max_length=200), blank=False)
    subjects = ArrayField(models.CharField(max_length=100), blank=False)
    tags = ArrayField(models.CharField(max_length=100), blank=True)
    setname = models.CharField(max_length=50, blank=True)
    items = models.IntegerField(default=0)
    mark = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    hascq = models.BooleanField(default=False)
    hasmcq = models.BooleanField(default=False)
    cqelist = ArrayField(models.IntegerField(default=0), blank=True)
    mcqelist = ArrayField(models.IntegerField(default=0), blank=True)
    # open for all user
    OPEN = 'o'
    # only who have permission
    CLOSED = 'c'
    # only owner
    PRIVATE = 'p'
    PRIVACY_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
        (PRIVATE, 'Private'),
    )
    privacy = models.CharField(
        max_length=1,
        choices=PRIVACY_CHOICES,
        default=OPEN,
    )
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("exam:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]
