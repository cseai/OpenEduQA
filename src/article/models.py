import time
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from notifications.signals import notify
from django.dispatch import receiver

from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from django.contrib.postgres.fields import ArrayField

# from level.models import Level
from course.models import Subject


from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time
# Create your models here.
# MVC MODEL VIEW CONTROLLER


class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        # Article.objects.all() = super(ArticleManager, self).all()
        return super(ArticleManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    ArticleModel = instance.__class__
    new_id = ArticleModel.objects.order_by("id").last().id + 1
    app_name = "article"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class Article(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True) #assume minutes
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # level = models.ForeignKey(Level, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=200), blank=True)

    objects = ArticleManager()

    # def __unicode__(self):
    #     return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        '''[summary]

        [description]
        Returns:
            [type] -- [returns markdown content that means original content]
        '''
        content = self.content
        return content

    def get_html(self):
        '''[summary]

        [description]

        Returns:
            [type] -- [returns converted html content from markdown content]
        '''
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    print(slug)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        # new_slug = "%s-%s" % (slug, qs.first().id)
        new_slug = f"{slug}-{qs.first().id}"
        print('new_slug:', new_slug)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Article)
def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


# pre_save.connect(pre_save_article_receiver, sender=Article)


@receiver(post_save, sender=Article)
def post_save_article_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if instance.draft != True:
            verb = f"{instance.user.name} wrote an Article {instance.title}."
            data = {'url': instance.get_absolute_url()}
            notify.send(instance, recipient=instance.user.user_set, verb=verb, data=data)
        else:
            verb = f"Your article {instance.title} was saved as Draft! You can edit and publish it anytime."
            data = {'url': instance.get_absolute_url()}
            notify.send(instance, recipient=instance.user, verb=verb, data=data)
    else:
        if instance.draft != True:
            try:
                recipient_users = instance.user.user_set.all()
            except:
                recipient_users = None
            if recipient_users:
                verb = f"{instance.user.name} edited the article {instance.title}."
                data = {'url': instance.get_absolute_url()}
                notify.send(instance, recipient=recipient_users, verb=verb, data=data)

            verb = f"Your article {instance.title} updated successfully."
            data = {'url': instance.get_absolute_url()}
            notify.send(instance, recipient=instance.user, verb=verb, data=data)

        else:
            verb = f"Your article {instance.title} updated as draft. You can always publish it."
            data = {'url': instance.get_absolute_url()}
            notify.send(instance, recipient=instance.user, verb=verb, data=data)
