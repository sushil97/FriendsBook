# Generated by Django 2.1.5 on 2019-10-23 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20191023_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofileinfo',
            name='fee',
            field=models.IntegerField(default=0),
        ),
    ]