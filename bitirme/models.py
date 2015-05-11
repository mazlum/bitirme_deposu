# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models.loading import get_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from validators import *
from random import choice
from string import ascii_letters, digits
from os import path
from autoslug import AutoSlugField

SEX = (
    ('M', 'Erkek'),
    ('F', 'Bayan'),
)

GRADE = (
    (0, 'Hazırlık'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4')
)


def profile_file_name(instance, filename):
    file_n, file_extension = path.splitext(filename)
    return path.join('profile', ''.join([choice(ascii_letters + digits) for n in xrange(30)]) + file_extension)


def file_name(instance, filename):
    file_n, file_extension = path.splitext(filename)
    return path.join('file', '{0}_{1}{2}'.format(file_n, ''.join([choice(ascii_letters + digits) for n in xrange(10)]),
                                                 file_extension))


def image_name(instance, filename):
    file_n, file_extension = path.splitext(filename)
    return path.join('image', '{0}_{1}{2}'.format(file_n, ''.join([choice(ascii_letters + digits) for n in xrange(10)]),
                                                  file_extension))


class City(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Users(User):
    image = models.ImageField(upload_to=profile_file_name, validators=[validate_file, validate_file_size],
                              default='profile/profile.png', blank=True, null=True)
    university = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    grade = models.PositiveSmallIntegerField(choices=GRADE)
    city = models.ForeignKey(City)
    sex = models.CharField(max_length=2, choices=SEX)

    def get_sex(self):
        return self.sex


class File(models.Model):
    file = models.FileField(upload_to=file_name, validators=[validate_thesis_file, validate_thesis_file_size])


class Image(models.Model):
    image = models.ImageField(upload_to=image_name, validators=[validate_file, validate_thesis_image_size])


class Thesis(models.Model):
    user = models.ForeignKey(Users)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', editable=True)
    content = models.TextField()
    image = models.ManyToManyField(Image)
    file = models.ManyToManyField(File)


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class