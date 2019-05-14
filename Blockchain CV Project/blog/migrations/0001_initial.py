# Generated by Django 2.2 on 2019-05-14 11:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.TextField()),
                ('idOfCandidate', models.DecimalField(decimal_places=0, max_digits=10000)),
                ('idOfEmployer', models.DecimalField(decimal_places=0, max_digits=10000)),
            ],
        ),
        migrations.CreateModel(
            name='employer_education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('fname', models.CharField(max_length=50)),
                ('sname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateTimeField(default=django.utils.timezone.now)),
                ('roleOfUser', models.CharField(max_length=9)),
                ('ABN', models.DecimalField(decimal_places=0, max_digits=11)),
            ],
        ),
        migrations.CreateModel(
            name='employer_experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('sname', models.CharField(max_length=50)),
                ('stime', models.DateTimeField(default=django.utils.timezone.now)),
                ('ltime', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.CharField(max_length=50)),
                ('contribution', models.CharField(max_length=50)),
                ('comment_box', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('fname', models.CharField(max_length=50)),
                ('sname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('dateOfBirth', models.DateTimeField(default=django.utils.timezone.now)),
                ('roleOfUser', models.CharField(choices=[('1', 'Candidate'), ('2', 'Employer'), ('3', 'Education')], max_length=50)),
                ('medicare', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
    ]
