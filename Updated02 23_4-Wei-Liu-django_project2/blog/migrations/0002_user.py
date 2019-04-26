# Generated by Django 2.2 on 2019-04-26 08:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('fname', models.CharField(max_length=50)),
                ('sname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateTimeField(default=django.utils.timezone.now)),
                ('roleOfUser', models.CharField(max_length=9)),
            ],
        ),
    ]
