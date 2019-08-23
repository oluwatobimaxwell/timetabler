# Generated by Django 2.2.2 on 2019-08-12 09:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lecturers_mgt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturers',
            name='friFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='friTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='monFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='monTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='satFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='satTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='thuFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='thuTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='tueFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='tueTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='wedFrom',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturers',
            name='wedTo',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Conversation Time'),
            preserve_default=False,
        ),
    ]