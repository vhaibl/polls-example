# Generated by Django 2.2.10 on 2021-01-24 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='vote',
            new_name='many',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='choice',
            new_name='one',
        ),
    ]
