# Control de Cambios Django Module

Este documento describe la aplicación de Control de Cambios desarrollada con Django, incluyendo detalles sobre la administración del modelo, campos y funcionalidades administrativas.

## Tabla de Contenidos
- [Introducción](#introducción)
- [Instalación](#instalación)
- [Configuración del Admin](#configuración-del-admin)
- [Modelos](#modelos)
- [Funcionalidades Administrativas](#funcionalidades-administrativas)
- [Cómo Contribuir](#cómo-contribuir)
- [Licencia](#licencia)

## Introducción
La aplicación de Control de Cambios está diseñada para gestionar y documentar los cambios en los sistemas o procesos de una organización. Facilita la supervisión, aprobación y comunicación de los cambios implicados.

## Instalación

Sigue estos pasos para instalar la aplicación:

```bash
git clone https://github.com/tu_usuario/control-de-cambios.git
cd control-de-cambios
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configuración del Admin

En `admin.py`, se definen las siguientes clases para la administración de los modelos:

### CustomControlAdmin

```python
class CustomControlAdmin(admin.ModelAdmin):
    list_display = ['Titulo', 'Ticket', 'Fecha', 'Supervisor', 'Decripcion_Corta']
    actions = [enviar_correo_control_de_cambios, generar_pdf_control_de_cambios]
    inlines = [EmailGroupMemberInline, ResponsablesInline]
    list_filter = ('Fecha', 'responsables', 'Supervisor')
    search_fields = ('responsables', 'Fecha')
    fieldsets = (
        (_('Documento'), {'fields': ('Titulo', 'Ticket', 'Fecha', 'Supervisor', 'Destinatarios_Correo')}),
        (_('Responsables'), {'fields': ('responsables',)}),
        (_('Información de trabajo para el control de cambios'), {'fields': ('Facilidad', 'Dispositivo', 'Decripcion_Corta', 'Objetivo', 'Impacto', 'Prioridad')}),
        (_('Logística y validación'), {'fields': ('Logistica_Validacion',)}),
        (_('Rollback'), {'fields': ('Procedimiento_Rollback',)}),
        (_('Logística de pruebas de seguridad'), {'fields': ('Pruebas_Seguridad',)})
    )
    readonly_fields = ['Titulo', 'Destinatarios_Correo', 'responsables']
```

### ImpactoAdmin, PrioridadAdmin, AprobacionAdmin

```python
@admin.register(Impacto)
class ImpactoAdmin(admin.ModelAdmin):
    list_display = ['Titulo', 'Descripcion']

@admin.register(Prioridad)
class PrioridadAdmin(admin.ModelAdmin):
    list_display = ['Nivel', 'Descripcion']

@admin.register(Aprobacion)
class AprobacionAdmin(admin.ModelAdmin):
    list_display = ['Control', 'Aprobado_Por', 'Fecha']
    readonly_fields = ['Aprobado_Por', 'Fecha']
```

## Modelos

Los modelos principales incluyen Control, Impacto, Prioridad, Responsable, y Aprobacion. Estos están definidos en `models.py` y se relacionan con las funcionalidades administrativas del sistema.

## Funcionalidades Administrativas

- `enviar_correo_control_de_cambios`: Función para enviar detalles de los controles de cambios por correo electrónico.
- `generar_pdf_control_de_cambios`: Genera un PDF con los detalles del control de cambios seleccionado.

## Cómo Contribuir

1. Fork el repositorio.
2. Crea una nueva rama para tus cambios.
3. Haz tus cambios y haz un commit con un mensaje claro.
4. Envía un pull request con tus cambios.

## Licencia

Este proyecto se distribuye bajo la licencia MIT, lo que permite la reutilización con pocas restricciones.
