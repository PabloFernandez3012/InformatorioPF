# Generated by Django 5.2.4 on 2025-07-16 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tareas', '0006_juego_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juego',
            name='imagen',
            field=models.CharField(blank=True, choices=[('', 'Sin imagen')], default='', help_text='Selecciona una imagen de la carpeta static/img/games/', max_length=200, verbose_name='Imagen del juego'),
        ),
    ]
