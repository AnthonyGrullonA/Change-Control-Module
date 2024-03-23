# Generated by Django 5.0.3 on 2024-03-21 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_emailgroup'),
        ('cambio', '0013_remove_control_solicitud_delete_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='Destinatarios_Correo',
            field=models.ManyToManyField(blank=True, related_name='email_groups', to='authentication.emailgroup'),
        ),
    ]
