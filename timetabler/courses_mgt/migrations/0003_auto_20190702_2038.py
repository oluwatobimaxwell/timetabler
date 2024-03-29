# Generated by Django 2.2.2 on 2019-07-02 20:38

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0002_auto_20190701_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='preferedtime',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecturers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('LEC0001', 'Dr. Dioha Mike'), ('LEC0005', 'Engr. Daniel Mtselia'), ('LEC0006', 'Dr. Samuel Agada')], max_length=2048),
        ),
    ]
