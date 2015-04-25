# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showviewing',
            name='name',
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name='showviewing',
            unique_together=set([('show', 'name')]),
        ),
    ]
