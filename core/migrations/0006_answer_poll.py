# Generated by Django 2.2.10 on 2021-01-25 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210125_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Poll'),
        ),
    ]
