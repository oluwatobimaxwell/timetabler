# Generated by Django 2.2.2 on 2019-07-06 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0007_auto_20190704_1457'),
        ('tablegenerator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablesgenerated',
            name='course',
            field=models.ForeignKey(db_column='course', default=None, on_delete=django.db.models.deletion.CASCADE, to='courses_mgt.Course', to_field='code'),
        ),
    ]
