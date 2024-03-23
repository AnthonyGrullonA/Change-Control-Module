# Generated by Django 5.0.3 on 2024-03-19 20:07

import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(default='Formulario Control de Cambios | Interno | V4', max_length=100)),
                ('Ticket', models.CharField(max_length=100)),
                ('Fecha', models.DateTimeField()),
                ('Nombre_Completo', models.CharField(max_length=100)),
                ('Departamento', models.CharField(max_length=100)),
                ('Posicion', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Numero_Contacto', models.CharField(max_length=10)),
                ('Facilidad', models.CharField(choices=[('none', '. . .'), ('east', 'NAP EAST'), ('west', 'NAP WEST')], default='none', max_length=20)),
                ('Dispositivo', models.CharField(max_length=100)),
                ('Decripcion_Corta', models.CharField(max_length=150)),
                ('Objetivo', models.CharField(max_length=100)),
                ('Logistica_Validacion', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('Procedimiento_Rollback', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('Pruebas_Seguridado', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
            ],
        ),
        migrations.CreateModel(
            name='Impacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=100)),
                ('Descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Prioridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nivel', models.CharField(max_length=100)),
                ('Descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Aprobacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firma', models.ImageField(blank=True, null=True, upload_to='signs/')),
                ('Aprobado_Por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cambio.control')),
            ],
        ),
        migrations.AddField(
            model_name='control',
            name='Impacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cambio.impacto'),
        ),
        migrations.AddField(
            model_name='control',
            name='Prioridad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cambio.prioridad'),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Titulo', models.CharField(max_length=100)),
                ('Descripcion', models.TextField()),
                ('Solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
