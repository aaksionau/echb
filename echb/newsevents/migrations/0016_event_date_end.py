# Generated by Django 2.0.7 on 2018-12-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsevents', '0015_auto_20181001_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_end',
            field=models.DateField(null=True),
        ),
    ]