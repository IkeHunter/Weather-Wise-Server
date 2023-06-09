# Generated by Django 3.2.18 on 2023-04-24 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0006_auto_20230423_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('location', models.IntegerField(primary_key=True, serialize=False)),
                ('archive_end', models.BigIntegerField(default=0)),
                ('archive_start', models.BigIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
