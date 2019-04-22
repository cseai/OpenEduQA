import time
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db import models

from django.conf import settings
from django.utils.safestring import mark_safe

from markdown_deux import markdown

from course.models import Subject


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    McqModel = instance.__class__
    new_id = McqModel.objects.order_by("id").last().id + 1
    app_name = "mcq"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Mcq(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

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

    choices = ArrayField(
        models.CharField(max_length=500),  # 120
        size=10,
    )
    answer = ArrayField(
        models.IntegerField(),
        size=10,
    )

    # level = models.ForeignKey(Level, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
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
        return reverse("mcq:detail", kwargs={"id": self.id})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def answer_text(self):
        content = []
        for ans in self.answer:
            content.append(self.choices[ans - 1])
        return content

    def get_markdown_question(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]
        '''
        content = self.question
        return content

    def get_markdown_choices(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]
        '''
        content = []
        for choice in self.choices:
            content.append(choice)
        # content = self.choices
        return content

    def get_markdown_answer(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]


        ## [get-len-of-the-arrayfield-postgres-django](https://stackoverflow.com/questions/35621502/get-len-of-the-arrayfield-postgres-django)
            If you are sure your array is 1-dimensional, you can use PostgreSQL function cardinality

            ModelA.objects.extra(select={'length':'cardinality(field1)'}).order_by('length')
            Or, using array_length function (with second argument being the number of dimensions sought)

            ModelA.objects.extra(select={'length':'array_length(field1,1)'}).order_by('length')
        '''
        content = []
        for ans in self.answer:
            content.append(self.choices[ans - 1])

        return content

    def get_answer_len(self):
        anslen = len(self.answer)
        # print("anslen = ", anslen)
        return anslen

    def get_html_question(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = self.question
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_html_choices(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = []
        for choice in self.choices:
            content.append(mark_safe(markdown(choice)))
        return content

    def get_html_answer(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = []
        for ans in self.answer:
            content.append(mark_safe(markdown(self.choices[ans - 1])))
        return content
