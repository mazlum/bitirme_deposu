# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bitirme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='slug',
            field=autoslug.fields.AutoSlugField(),
        ),
    ]
