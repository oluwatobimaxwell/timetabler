# Generated by Django 2.2.2 on 2019-08-13 08:57

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses_mgt', '0014_auto_20190812_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lecturers',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('LEC0001', 'David Mark'), ('LEC0002', 'Angela Kelly'), ('LEC0003', 'Eleanar james'), ('LEC0004', 'Blessing Okorikoko'), ('LEC0005', 'Dr. Dioha Mike'), ('LEC0006', 'Blessing Okorikoko'), ('LEC0008', 'Benjamin'), ('LEC0009', 'Jaferson'), ('LEC0010', 'Andrew K'), ('LEC0011', 'Philipo I'), ('LEC0012', 'James Akme'), ('LEC0013', 'Abdul Sam'), ('LEC0014', 'Donald P'), ('LEC0015', 'Edward Calistus'), ('LEC0016', 'Samuel L'), ('LEC0017', 'Eddie Lamb'), ('LEC0018', 'Anthony'), ('LEC0019', 'Steward Kelan'), ('LEC0020', 'Joam Hebrew'), ('LEC0021', 'Edwardo M'), ('LEC0022', 'Bularg P'), ('LEC0023', 'Angellina'), ('LEC0024', 'EBrew Jackson'), ('LEC0025', 'Samuel L. Jackson')], max_length=2048),
        ),
    ]
