# Generated by Django 2.1.7 on 2019-05-28 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190528_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='medicare',
        ),
    ]
