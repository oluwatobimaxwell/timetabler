# Generated by Django 2.2.2 on 2019-07-03 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues_mgt', '0009_auto_20190703_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='reservedDays',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedDepartment',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedFaculty',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedLevel',
            field=models.CharField(max_length=2048),
        ),
    ]
