# Generated by Django 2.2.24 on 2021-07-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='cuidad',
            field=models.CharField(default=False, max_length=80),
        ),
    ]