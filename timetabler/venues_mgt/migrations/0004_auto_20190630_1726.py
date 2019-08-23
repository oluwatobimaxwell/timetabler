# Generated by Django 2.2.2 on 2019-06-30 17:26

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('venues_mgt', '0003_auto_20190630_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='reservedDays',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Mon', 'Mondays'), ('Tue', 'Tuesdays'), ('Wed', 'Wednesdays'), ('Thu', 'Thurdays'), ('Fri', 'Fridays'), ('Sat', 'Saturday')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedDepartment',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('DPT001', 'Computer Engineering'), ('DPT005', 'Electrical & Electronics Engineering'), ('DPT006', 'Mechanical Engineering'), ('DPT007', 'Telecommunications Engineering'), ('DPT008', 'Civil Engineering'), ('DPT009', 'Petroleum Engineering'), ('DPT013', 'Law LLB'), ('DPT014', 'Business Law LLB'), ('DPT015', 'Private and Public Law LLB')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedFaculty',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('FAC01', 'Faculty of Engineering'), ('FAC20', 'Faculty of Law'), ('FAC21', 'Computer Science and IT')], max_length=2048),
        ),
        migrations.AlterField(
            model_name='venue',
            name='reservedLevel',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(100, '100 Level'), (200, '200 Level'), (300, '300 Level'), (400, '400 Level'), (500, '500 Level')], max_length=2048),
        ),
    ]