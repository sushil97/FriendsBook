# Generated by Django 2.0.5 on 2019-10-30 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0017_userprofileinfo_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='user_type',
            field=models.CharField(default='Casual', max_length=30),
        ),
    ]
