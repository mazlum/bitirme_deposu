# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bitirme', '0003_auto_20150430_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='grade',
            field=models.PositiveSmallIntegerField(choices=[(0, b'Haz\xc4\xb1rl\xc4\xb1k'), (1, b'1'), (2, b'2'), (3, b'3'), (4, b'4')]),
        ),
    ]
