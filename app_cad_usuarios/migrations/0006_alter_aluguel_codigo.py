# Generated by Django 5.1.3 on 2024-11-17 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cad_usuarios', '0005_aluguel_devolvida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluguel',
            name='codigo',
            field=models.CharField(max_length=6),
        ),
    ]
