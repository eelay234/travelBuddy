# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 17:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100)),
                ('from_date', models.DateField(default=datetime.date.today)),
                ('to_date', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='planner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planner', to='travel.User'),
        ),
        migrations.AddField(
            model_name='trip',
            name='turists',
            field=models.ManyToManyField(related_name='turists', to='travel.User'),
        ),
    ]
