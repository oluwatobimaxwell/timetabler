# Generated by Django 2.2.2 on 2019-08-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablegenerator', '0002_tablesgenerated_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablesgenerated',
            name='remarks',
            field=models.CharField(default='', max_length=2048),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tablesgenerated',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tablesgenerated',
            name='students',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
