# Generated by Django 3.1.2 on 2022-02-27 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20220227_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='tag_select',
        ),
    ]
