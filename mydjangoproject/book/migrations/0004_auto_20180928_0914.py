# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_remove_bookinfo_bpic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroinfo',
            name='hpic',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
