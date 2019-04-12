from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import User


# @receiver(post_save, sender=User)
# def my_handler(sender, **kwargs):
#     print(sender, kwargs)
