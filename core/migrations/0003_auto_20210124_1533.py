# Generated by Django 2.2.10 on 2021-01-24 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210124_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='many',
            field=models.ManyToManyField(null=True, related_name='answers', to='core.Choice'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='one',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Choice'),
        ),
    ]