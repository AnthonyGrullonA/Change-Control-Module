# Generated by Django 5.0.3 on 2024-03-20 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cambio', '0004_alter_control_solicitud_alter_control_supervisor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aprobacion',
            name='Firma',
        ),
    ]
