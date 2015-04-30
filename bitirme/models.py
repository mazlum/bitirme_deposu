from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models.loading import get_model
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SEX = (
    ('M', 'Erkek'),
    ('F', 'Bayan'),
)


class City(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Users(User):
    university = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    grade = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City)
    sex = models.CharField(max_length=2, choices=SEX)


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