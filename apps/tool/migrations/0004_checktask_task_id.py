# Generated by Django 3.1.3 on 2021-10-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_auto_20211015_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='checktask',
            name='task_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='任务id'),
        ),
    ]
