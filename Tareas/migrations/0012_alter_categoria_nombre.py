# Generated by Django 5.2.4 on 2025-07-16 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tareas', '0011_juego_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(help_text='Escribe el nombre de la categoría (ej: Disparos, RPG, Aventura, etc.)', max_length=50, unique=True),
        ),
    ]
