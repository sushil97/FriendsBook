# Generated by Django 2.0.5 on 2019-10-30 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0019_auto_20191027_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupprofileinfo',
            name='type',
        ),
    ]
