# Generated by Django 2.2.24 on 2021-07-18 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('casas', '0002_inmueble_cuidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='casas.Estado')),
            ],
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='cuidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='casas.Ciudad', verbose_name='Entidad federativa'),
        ),
    ]