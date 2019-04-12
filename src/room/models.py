from django.db import models
from django.contrib.postgres.fields import ArrayField
import time
from django.conf import settings
from django.urls import reverse

from exam.models import Exam
from teacher.models import Teacher
from student.models import Student
# Create your models here.


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    RoomModel = instance.__class__
    new_id = RoomModel.objects.order_by("id").last().id + 1
    app_name = "room"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Room(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='room_user', on_delete=models.CASCADE)
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

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, blank=False)
    students = models.ManyToManyField(Student, blank=False)
    tags = ArrayField(models.CharField(max_length=100), blank=True)
    duration = models.IntegerField(default=0)
    happen = models.DateTimeField(auto_now=False, auto_now_add=False)

    # all student can attend this room
    OPEN = 'o'
    # student can see the room and request to enroll AND if teacher accept the request then can attend
    CLOSED = 'c'
    # student can see the room but teacher can add student and then only added studen can attend to the room
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
        return reverse("room:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]
