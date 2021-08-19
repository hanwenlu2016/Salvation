# Generated by Django 3.1.3 on 2021-08-18 14:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0002_auto_20210818_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='prjcet_participant',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='项目参与者'),
        ),
    ]