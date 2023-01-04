# -*- coding: utf-8 -*-
import datetime
from django.db import models, migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='namer_computergroup',
            fields=[
                ('id', models.AutoField(verbose_name='id',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('prefix', models.CharField(max_length=200, null=True, blank=True)),
                ('domain', models.CharField(max_length=200, null=True, blank=True)),
                ('key', models.CharField(max_length=255, unique=True, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='namer_computer',
            fields=[
                ('id', models.AutoField(verbose_name='id',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('computergroup', models.CharField(max_length=200)),
                ('name', models.ForeignKey(to='namer.MachineGroup', on_delete=models.CASCADE, max_length=200, null=True, blank=True)),
                ('serial', models.CharField(default='abc', max_length=200, unique=True)),
                ('last_checkin', models.CharField(default=datetime.datetime(2012, 10, 10, 0, 0), null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='namer_network',
            fields=[
                ('id', models.AutoField(verbose_name='id',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('network', models.CharField(max_length=200, unique=True)),
                ('computergroup', models.ForeignKey(to='namer.ComputerGroup', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['network'],
            },
        ),
    ]