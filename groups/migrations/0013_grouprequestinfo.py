# Generated by Django 2.1.5 on 2019-10-24 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('groups', '0012_auto_20191024_0109'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRequestInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('rejected', models.DateTimeField(blank=True, null=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_requests_sent', to=settings.AUTH_USER_MODEL)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('to_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_requests_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]