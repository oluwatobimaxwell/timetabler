# Generated by Django 2.2.2 on 2019-07-04 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0007_auto_20190704_1457'),
        ('departments_mgt', '0004_auto_20190703_1254'),
        ('enrollment', '0004_auto_20190704_2251'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Enrollment',
            new_name='Enrolment',
        ),
    ]
