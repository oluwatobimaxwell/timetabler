# Generated by Django 2.2.2 on 2019-07-03 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments_mgt', '0002_auto_20190703_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(db_column='faculty', default=None, on_delete=django.db.models.deletion.CASCADE, to='faculty_mgt.Faculty'),
        ),
    ]
