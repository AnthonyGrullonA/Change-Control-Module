from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Aprobacion, Control, Departamento, Impacto, Prioridad, Responsable
from .admin_function import enviar_correo_control_de_cambios, generar_pdf_control_de_cambios
from authentication.models import EmailGroup

class EmailGroupMemberInline(admin.TabularInline):
    model = Control.Destinatarios_Correo.through
    extra = 1
    verbose_name_plural = 'Destinatarios'

class ResponsablesInline(admin.TabularInline):
    model = Control.responsables.through
    extra = 1
    verbose_name_plural = 'Responsables'
    
class CustomControlAdmin(admin.ModelAdmin):
    list_display = ['Titulo', 'Ticket', 'Fecha', 'Supervisor', 'Decripcion_Corta']
    actions = [enviar_correo_control_de_cambios, generar_pdf_control_de_cambios]
    inlines = (EmailGroupMemberInline, ResponsablesInline)
    list_filter = ('Fecha', 'responsables', 'Supervisor', )
    search_fields = ('responsables', 'Fecha')

    fieldsets = (
        (_('Documento'), {'fields': ('Titulo', 'Ticket', 'Fecha', 'Supervisor', 'Destinatarios_Correo',)}),
        (_('Responsables'), {'fields': ('responsables', )}),
        (_('Información de trabajo para el control de cambios'), {'fields': ('Facilidad', 'Dispositivo', 'Decripcion_Corta', 'Objetivo', 'Impacto', 'Prioridad')}),
        (_('Logística y validación'), {'fields': ('Logistica_Validacion',)}),
        (_('Rollback'), {'fields': ('Procedimiento_Rollback',)}),
        (_('logistica de pruebas de seguridad'), {'fields': ('Pruebas_Seguridado',)}),
    )
    
    readonly_fields = ['Titulo', 'Destinatarios_Correo', 'responsables']


# Registrar los modelos y el admin personalizado en el sitio de administración
admin.site.register(Control, CustomControlAdmin)

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

    def save_model(self, request, obj, form, change):
        if not obj.Aprobado_Por_id:
            obj.Aprobado_Por = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['Control']
        return self.readonly_fields

# Reemplaza el registro de ControlAdmin con CustomControlAdmin
admin.site.unregister(Control)
admin.site.register(Control, CustomControlAdmin)
admin.site.register(Departamento)
admin.site.register(Responsable)