# Generated by Django 4.1.7 on 2023-03-01 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baedal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='password',
            field=models.CharField(max_length=300),
        ),
    ]