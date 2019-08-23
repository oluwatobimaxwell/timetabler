# Generated by Django 2.2.2 on 2019-07-01 03:14

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='departments',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('DPT001', 'Computer Engineering'), ('DPT005', 'Electrical & Electronics Engineering'), ('DPT006', 'Mechanical Engineering'), ('DPT007', 'Telecommunications Engineering'), ('DPT008', 'Civil Engineering'), ('DPT009', 'Petroleum Engineering')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecturers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('LEC0001', 'Dr. Dioha Mike'), ('LEC0005', 'Engr. Daniel Mtselia')], max_length=2048),
        ),
    ]
