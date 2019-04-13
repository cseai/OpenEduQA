# accounts.models.py
import time
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from notifications.signals import notify


from teacher.models import Teacher
from student.models import Student

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

# accounts.models.py


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    new_filename = f"{ int(time.time() * 1000) }_{filebase}.{extension}"
    # id genaration have some problem so don't use it
    # UserModel = instance.__class__
    # new_id = UserModel.objects.order_by("id").last().id + 1
    new_id = 'profile_img'
    app_name = "accounts"
    return "%s/%s/%s" % (app_name, new_id, new_filename)


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=32,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alphanumeric or contain numbers',
                code='invalid_username'
            )],
        unique=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    name = models.CharField(max_length=40, blank=True)

    MALE = 'm'
    FEMALE = 'f'
    OTHERS = 'o'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MALE
    )

    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    birth_date_public = models.BooleanField(default=False)

    current_address = models.CharField(max_length=255, blank=True)
    parmanent_address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        default='default.png',
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    bio = models.TextField(blank=True)

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.
    #
    # Teacher, Student, Guardian
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=True)
    follows = models.ManyToManyField("User", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def get_absolute_url(self):
        return reverse("accounts:profile")

    def get_user_url(self):
        return reverse("accounts:user", kwargs={'id': self.id})

    def get_profile_update_url(self):
        return reverse("accounts:profile_update")

    def get_full_name(self):
        # The user is identified by their email address
        if self.name:
            return self.name
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        return self.staff

    @property
    def is_superuser(self):
        # "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        # "Is the user active?"
        return self.active


@receiver(pre_save, sender=User)
def pre_save_user_receiver(sender, instance, *args, **kwargs):
    # if the user is a teacher/student then need to update the teacher/student model/table too
    if instance:
        if instance.is_guest and (instance.is_teacher or instance.is_student or instance.is_superuser or instance.is_staff):
            instance.is_guest = False
        elif not instance.is_guest and not (instance.is_teacher or instance.is_student or instance.is_superuser or instance.is_staff):
            instance.is_guest = True

        print("pre_save_user_receiver -> OK")
    else:
        print("pre_save_user_receiver -> instance was None!")


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    # if the user is a teacher/student then need to update the teacher/student model/table too
    if instance:
        # teacher_obj = Teacher.objects.filter(user=instance).first()
        # student_obj = Student.objects.filter(user=instance).first()
        try:
            teacher_obj = instance.teacher
        except AttributeError:
            teacher_obj = None
            print('instance teacher_obj is', teacher_obj)

        try:
            student_obj = instance.student
        except AttributeError:
            student_obj = None
            print('instance student_obj is', student_obj)
        if instance.is_teacher:
            if teacher_obj:
                if not teacher_obj.is_active:
                    teacher_obj.active = True
                    teacher_obj.save()
                    print("teacher is_active was False and now it is ", teacher_obj.is_active)
            else:
                # Any keyword arguments passed to get_or_create() — except an optional one called defaults — will be used in a get() call.
                # If an object is found, get_or_create() returns a tuple of that object and False.
                teacher_obj, t_created = Teacher.objects.get_or_create(user=instance)

        elif teacher_obj and teacher_obj.is_active:
            teacher_obj.active = False
            teacher_obj.save()

        if instance.is_student:
            if student_obj:
                if not student_obj.is_active:
                    student_obj.active = True
                    student_obj.save()
                    print("student is_active was False and now it is", student_obj.is_active)
            else:
                student_obj, s_created = Student.objects.get_or_create(user=instance)
        elif student_obj and student_obj.is_active:
            student_obj.active = False
            student_obj.save()

        print("post_save_user_receiver done!")
        if created:
            verb = f"Hi {instance.name}, your account has been created! Now update your profile info."
            data = {'url': instance.get_profile_update_url()}
            notify.send(instance, recipient=instance, verb=verb, data=data)
        else:
            verb = f"Hi {instance.name}, your profile updation has been saved!"
            data = {'url': instance.get_user_url()}
            print(data)
            notify.send(instance, recipient=instance, verb=verb, data=data)

    else:
        print("post_save_user_receiver instance is None!")


# pre_save.connect(pre_save_user_receiver, sender=User)
# post_save.connect(post_save_user_receiver, sender=User)
