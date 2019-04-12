import time
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db import models

from django.conf import settings
from django.utils.safestring import mark_safe

from course.models import Subject

from markdown_deux import markdown
# Create your models here.


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    CqModel = instance.__class__
    new_id = CqModel.objects.order_by("id").last().id + 1
    app_name = "cq"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Cq(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # related_name='cq_user',

    question = models.TextField()

    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    answer = models.TextField()

    # level = models.ForeignKey(Level, related_name='cq_level', on_delete=models.CASCADE)  # related_name='cq_level',
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # related_name='cq_subject',
    tags = ArrayField(models.CharField(max_length=200), blank=True)
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
        return self.question

    def get_absolute_url(self):
        return reverse("cq:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown_question(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]
        '''
        content = self.question
        return content

    def get_markdown_answer(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]
        '''
        content = self.answer
        return content

    def get_html_question(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = self.question
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_html_answer(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = mark_safe(markdown(self.answer))
        return content
