# Generated by Django 2.2.2 on 2019-07-03 20:31

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0005_auto_20190703_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='departments',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('DPT001', 'Computer Engineering'), ('DPT034', 'Civil Engineering'), ('DPT035', 'Mechanical Engineering'), ('DPT036', 'Telecommunications Engineering'), ('DPT037', 'Petroleum Engineering'), ('DPT038', 'Electrical & Electronics Engineering'), ('DPT039', 'Law LLB')], max_length=2048),
        ),
    ]