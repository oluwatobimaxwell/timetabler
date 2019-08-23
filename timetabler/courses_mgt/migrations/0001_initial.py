# Generated by Django 2.2.2 on 2019-07-01 03:05

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('coursehourperweek', models.IntegerField(default=2)),
                ('semester', models.IntegerField(default=0)),
                ('departments', multiselectfield.db.fields.MultiSelectField(max_length=2048)),
                ('lecturers', multiselectfield.db.fields.MultiSelectField(max_length=2048)),
            ],
        ),
    ]
