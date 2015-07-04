# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AjaxData', '0002_userstats_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstats',
            name='timestamp',
            field=models.TextField(default='{time}'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userstats',
            name='currentViewers',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='followers',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='totalViews',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='username',
            field=models.TextField(),
        ),
    ]
