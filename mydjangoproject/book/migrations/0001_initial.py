# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('btitle', models.CharField(max_length=100)),
                ('bpubdate', models.DateTimeField(null=True)),
                ('bread', models.IntegerField(default=0)),
                ('bcomment', models.IntegerField(default=0)),
                ('bpic', models.ImageField(upload_to='images/')),
                ('isdelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '书',
                'verbose_name_plural': '书',
            },
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=100, verbose_name='姓名')),
                ('hgender', models.BooleanField(verbose_name='性别')),
                ('hcontent', models.TextField()),
                ('bpic', models.ImageField(upload_to='images/')),
                ('isdelete', models.BooleanField(default=False)),
                ('hbookinfo', models.ForeignKey(to='book.BookInfo')),
            ],
            options={
                'verbose_name': '英雄人物',
                'verbose_name_plural': '英雄人物',
                'ordering': ['-id', 'hname'],
            },
        ),
    ]
