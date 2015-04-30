# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bitirme', '0002_auto_20150430_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.CharField(max_length=2, choices=[(b'M', b'Erkek'), (b'F', b'Bayan')]),
        ),
    ]
