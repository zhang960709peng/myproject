# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(verbose_name='username', unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', related_query_name='user', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', related_query_name='user', blank=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'df_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
