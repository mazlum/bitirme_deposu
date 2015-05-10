# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings
import bitirme.validators
import bitirme.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pdf', models.FileField(upload_to=bitirme.models.file_name, validators=[bitirme.validators.validate_thesis_file, bitirme.validators.validate_thesis_file_size])),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=bitirme.models.image_name, validators=[bitirme.validators.validate_file, bitirme.validators.validate_thesis_image_size])),
            ],
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('file', models.ManyToManyField(to='bitirme.File')),
                ('image', models.ManyToManyField(to='bitirme.Image')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', models.ImageField(default=b'profile/profile.png', validators=[bitirme.validators.validate_file, bitirme.validators.validate_file_size], upload_to=bitirme.models.profile_file_name, blank=True, null=True)),
                ('university', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('grade', models.PositiveSmallIntegerField(choices=[(0, b'Haz\xc4\xb1rl\xc4\xb1k'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4')])),
                ('sex', models.CharField(max_length=2, choices=[(b'M', b'Erkek'), (b'F', b'Bayan')])),
                ('city', models.ForeignKey(to='bitirme.City')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='thesis',
            name='user',
            field=models.ForeignKey(to='bitirme.Users'),
        ),
    ]
