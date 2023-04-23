# Generated by Django 3.2.18 on 2023-04-22 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0002_auto_20230421_0433'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresults',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='searchresults',
            name='location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='logic.summary'),
            preserve_default=False,
        ),
    ]