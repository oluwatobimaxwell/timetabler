# Generated by Django 2.2.2 on 2019-07-03 05:45

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0003_auto_20190702_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='departments',
            field=multiselectfield.db.fields.MultiSelectField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecturers',
            field=multiselectfield.db.fields.MultiSelectField(max_length=2048),
        ),
    ]
