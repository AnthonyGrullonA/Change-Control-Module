from django.db import models
from authentication.models import CustomUser as User, EmailGroup
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Impacto(models.Model):
    Titulo = models.CharField(max_length=100)
    Descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.Titulo}"
    
    class Meta:
        verbose_name = "Impacto"
        verbose_name_plural = "Impactos"

class Prioridad(models.Model):
    Nivel = models.CharField(max_length=100)
    Descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.Nivel}"
    
    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"

class Departamento(models.Model):
    Nombre_Departamento = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Nombre_Departamento
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamento"
        
        
class Responsable(models.Model):
    nombre_completo = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    posicion = models.CharField(max_length=100)
    email = models.EmailField()
    numero_contacto = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.nombre_completo} - {self.posicion}'
    
    class Meta:
        verbose_name = "Responsable"
        verbose_name_plural = "Responsable"
        
    
class Control(models.Model):
    ESTADO_CHOICES = [
        ('none', '. . .'),
        ('east', 'NAP EAST'),
        ('west', 'NAP WEST')
    ]    
    #Seccion de titulo 

    Titulo = models.CharField(max_length=100, default='Formulario Control de Cambios | Interno | V4')
    Ticket = models.CharField(max_length=100)
    Fecha = models.DateField()
    Supervisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #Responsables
    
    responsables = models.ManyToManyField(Responsable)

    #Informacion de trabajo para el control de cambios
    
    Facilidad = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='none')
    Dispositivo = models.CharField(max_length=100)
    Decripcion_Corta = models.CharField(max_length=150)
    Objetivo = models.CharField(max_length=100)
    Impacto = models.ForeignKey(Impacto, on_delete=models.CASCADE)
    Prioridad = models.ForeignKey(Prioridad, on_delete=models.CASCADE)
    
    #Logistica y validacion
    Logistica_Validacion = CKEditor5Field('Text', config_name='default')
    
    #Rollback
    Procedimiento_Rollback = CKEditor5Field('Text', config_name='default')
    
    #Pruebas de seguridad
    Pruebas_Seguridado = CKEditor5Field('Text', config_name='default')
    
    Destinatarios_Correo = models.ManyToManyField(EmailGroup, related_name='email_groups', blank=True)
    
    def __str__(self):
        return f"{self.Titulo} - {self.Ticket} | {self.Nombre_Completo} - {self.Departamento}"
    
    class Meta:
        verbose_name = "Control de cambios"
        verbose_name_plural = "Controles de cambios"

class Aprobacion(models.Model):
    Control = models.ForeignKey(Control, on_delete=models.CASCADE)
    Aprobado_Por = models.ForeignKey(User, on_delete=models.CASCADE)
    Fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.Control)
    
    class Meta:
        verbose_name = "Aprobacion"
        verbose_name_plural = "Aprobaciones"

