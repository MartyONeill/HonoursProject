# Generated by Django 3.1.2 on 2022-01-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20220128_2000'),
        ('mezza', '0006_auto_20220129_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='event_applicants', to='account.Talent'),
        ),
    ]
