# Generated by Django 3.1.2 on 2022-01-26 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mezza', '0002_talent_instrument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='venue',
            name='user',
        ),
        migrations.DeleteModel(
            name='Talent',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]
