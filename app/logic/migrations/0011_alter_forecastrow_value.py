# Generated by Django 3.2.18 on 2023-04-27 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0010_alter_forecastrow_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastrow',
            name='value',
            field=models.FloatField(default=0.0),
        ),
    ]
