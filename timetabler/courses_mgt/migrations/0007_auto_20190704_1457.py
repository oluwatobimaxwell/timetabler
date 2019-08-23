# Generated by Django 2.2.2 on 2019-07-04 14:57

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0006_auto_20190703_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('LEC0001', 'Dr. Dioha Mike'), ('LEC0011', 'Mr Dansel')], max_length=2048),
        ),
    ]
