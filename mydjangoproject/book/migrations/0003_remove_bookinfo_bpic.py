# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20180927_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookinfo',
            name='bpic',
        ),
    ]
