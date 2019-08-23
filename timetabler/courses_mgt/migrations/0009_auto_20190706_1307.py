# Generated by Django 2.2.2 on 2019-07-06 13:07

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0008_auto_20190706_1258'),
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
