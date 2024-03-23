import os
from bs4 import BeautifulSoup
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import pdfkit
from django.http import HttpResponse
from django.utils.text import slugify

####################################################################

import os
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from bs4 import BeautifulSoup
import pdfkit

def generar_pdf_control_de_cambios(modeladmin, request, queryset):
    def get_email_groups(control):
        # Esta función recopila todos los correos de los grupos asociados y los devuelve
        email_groups = control.Destinatarios_Correo.all()
        emails = []
        for group in email_groups:
            emails.extend([member.email for member in group.members.all()])
        return emails  # Devuelve una lista de correos electrónicos 

    for control in queryset:
        # Analiza el HTML de Logistica_Validacion y Procedimiento_Rollback para obtener las imágenes
        soup_logistica = BeautifulSoup(control.Logistica_Validacion, 'html.parser')
        img_tags_logistica = soup_logistica.find_all('img')

        # Llamar a get_email_groups para obtener los correos para este control en particular
        destinatarios = get_email_groups(control)
        
        soup_rollback = BeautifulSoup(control.Procedimiento_Rollback, 'html.parser')
        img_tags_rollback = soup_rollback.find_all('img')

        soup_seguridad = BeautifulSoup(control.Pruebas_Seguridado, 'html.parser')
        img_tags_seguridad = soup_seguridad.find_all('img')
        
        # Creamos una lista para adjuntar todas las imágenes encontradas en ambos elementos
        images_to_attach = []

        # Función para procesar las imágenes y agregarlas a la lista de adjuntos
        def process_images(img_tags, prefix):
            for i, img in enumerate(img_tags, start=1):
                image_src = img['src']
                # Convertir la ruta absoluta a relativa
                image_path = os.path.relpath(image_src, start=os.path.dirname(__file__))
                images_to_attach.append((f'{prefix}_image{i}', image_path))
                img['src'] = f'cid:{prefix}_image{i}'

        # Procesa las imágenes de Logistica_Validacion y Procedimiento_Rollback
        process_images(img_tags_logistica, 'logistica')
        process_images(img_tags_rollback, 'rollback')
        process_images(img_tags_seguridad, 'seguridad')

        # Crear el contenido HTML para el cuerpo del PDF
        html_content = f'''
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
</head>
<body>
{destinatarios}
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <th colspan="4" style="border: 1px solid black; padding: 8px; background-color: #f2f2f2;">{control.Titulo} | {control.Ticket}</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Número de Ticket</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Ticket}</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Fecha}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Responsables</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Nombre</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Nombre_Completo}</td>
            <td style="border: 1px solid black; padding: 8px;">Departamento</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Departamento}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Email</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Email}</td>
            <td style="border: 1px solid black; padding: 8px;">Compañía</td>
            <td style="border: 1px solid black; padding: 8px;">NAP Del Caribe</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Tel. / Cel.</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Numero_Contacto}</td>
            <td colspan="2" style="border: 1px solid black; padding: 8px;"></td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Información del Trabajo Para Realizar</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Facilidad (SITE)</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Facilidad}</td>
            <td style="border: 1px solid black; padding: 8px;">Dispositivo</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Dispositivo}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Corta descripción</td>
            <td colspan="3" style="border: 1px solid black; padding: 8px;">{control.Decripcion_Corta}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Objetivo</td>
            <td colspan="3" style="border: 1px solid black; padding: 8px;">Alcances correspondientes para el funcionamiento del aplicativo appgate-SDP</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Impacto</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Impacto}</td>
            <td style="border: 1px solid black; padding: 8px;">Prioridad</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Prioridad}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Logística y Validación</strong></td>
        </tr>
                <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;">
                
            </td>
        </tr>

        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Procedimiento de Roll Back</strong></td>
        </tr>
        <tr>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Plan de Pruebas de Seguridad</strong></td>
        </tr>
        <tr>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Revisión Evaluación y Aprobación</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Solicitado por</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Nombre_Completo}</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Aprobada por</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
        </tr>
    </table>
</body>
</html>

        
        '''

        # Generar el nombre del archivo PDF
        pdf_filename = f'control_de_cambios_{slugify(control.Titulo)}_{control.id}.pdf'

        # Configurar pdfkit para usar wkhtmltopdf desde la ruta especificada
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

        # Generar el archivo PDF
        pdfkit.from_string(html_content, pdf_filename, configuration=config)

        # Abrir el archivo PDF generado y leer su contenido binario
        with open(pdf_filename, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        # Eliminar el archivo PDF después de leer su contenido
        os.remove(pdf_filename)

        # Crear la respuesta HTTP con el contenido del PDF para descargar
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

        return response

# Agregar la función a tu admin de Django
generar_pdf_control_de_cambios.short_description = 'Generar PDF de Control de Cambios'



####################################################################
def enviar_correo_control_de_cambios(modeladmin, request, queryset):
    def get_email_groups(control):
        # Esta función recopila todos los correos de los grupos asociados y los devuelve
        email_groups = control.Destinatarios_Correo.all()
        emails = []
        for group in email_groups:
            emails.extend([member.email for member in group.members.all()])
        return emails  # Devuelve una lista de correos electrónicos 

    for control in queryset:
        # Analiza el HTML de Logistica_Validacion y Procedimiento_Rollback para obtener las imágenes
        soup_logistica = BeautifulSoup(control.Logistica_Validacion, 'html.parser')
        img_tags_logistica = soup_logistica.find_all('img')

        # Llamar a get_email_groups para obtener los correos para este control en particular
        destinatarios = get_email_groups(control)
        
        soup_rollback = BeautifulSoup(control.Procedimiento_Rollback, 'html.parser')
        img_tags_rollback = soup_rollback.find_all('img')

        soup_seguridad = BeautifulSoup(control.Pruebas_Seguridado, 'html.parser')
        img_tags_seguridad = soup_seguridad.find_all('img')
        
        # Creamos una lista para adjuntar todas las imágenes encontradas en ambos elementos
        images_to_attach = []

        # Función para procesar las imágenes y agregarlas a la lista de adjuntos
        def process_images(img_tags, prefix):
            for i, img in enumerate(img_tags, start=1):
                image_src = img['src']
                image_path = os.path.join('media', os.path.basename(image_src))
                images_to_attach.append((f'{prefix}_image{i}', image_path))
                img['src'] = f'cid:{prefix}_image{i}'

        # Procesa las imágenes de Logistica_Validacion y Procedimiento_Rollback
        process_images(img_tags_logistica, 'logistica')
        process_images(img_tags_rollback, 'rollback')
        process_images(img_tags_seguridad, 'seguridad')

        # Crear el correo electrónico
        correo = EmailMultiAlternatives(
            subject='Detalle del Control de Cambios',
            body='',
            from_email='anthog@gmail.com',
            to=destinatarios
        )

        # Adjunta las imágenes encontradas en ambos elementos con encabezados adicionales
        for cid, image_path in images_to_attach:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{cid}>')
                image.add_header('Content-Disposition', 'inline')
                correo.attach(image)

        # Crea el contenido HTML para el cuerpo del correo
        # html_content = f'''
        #     <html>
        #     <body>
        #         <p>Logistica y validacion:</p>
        #         {soup_logistica.prettify()}
        #         <p>Procedimiento Rollback:</p>
        #         {soup_rollback.prettify()}
        #         <p>Texto adicional que quieras agregar.</p>
        #         <img src="cid:logistica_image1" alt="Logistica Image">
        #         <img src="cid:rollback_image1" alt="Rollback Image">
        #     </body>
        #     </html>
        # '''

        html_content = f'''
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
</head>
<body>
{destinatarios}
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <th colspan="4" style="border: 1px solid black; padding: 8px; background-color: #f2f2f2;">{control.Titulo} | {control.Ticket}</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Número de Ticket</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Ticket}</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Fecha}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Responsables</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Nombre</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Nombre_Completo}</td>
            <td style="border: 1px solid black; padding: 8px;">Departamento</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Departamento}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Email</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Email}</td>
            <td style="border: 1px solid black; padding: 8px;">Compañía</td>
            <td style="border: 1px solid black; padding: 8px;">NAP Del Caribe</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Tel. / Cel.</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Numero_Contacto}</td>
            <td colspan="2" style="border: 1px solid black; padding: 8px;"></td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Información del Trabajo Para Realizar</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Facilidad (SITE)</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Facilidad}</td>
            <td style="border: 1px solid black; padding: 8px;">Dispositivo</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Dispositivo}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Corta descripción</td>
            <td colspan="3" style="border: 1px solid black; padding: 8px;">{control.Decripcion_Corta}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Objetivo</td>
            <td colspan="3" style="border: 1px solid black; padding: 8px;">Alcances correspondientes para el funcionamiento del aplicativo appgate-SDP</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Impacto</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Impacto}</td>
            <td style="border: 1px solid black; padding: 8px;">Prioridad</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Prioridad}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Logística y Validación</strong></td>
        </tr>
                <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;">
                {soup_logistica.prettify()}
                
            </td>
        </tr>

        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Procedimiento de Roll Back</strong></td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;">{soup_rollback.prettify()}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Plan de Pruebas de Seguridad</strong></td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;">{soup_seguridad.prettify()}</td>
        </tr>
        <tr>
            <td colspan="4" style="border: 1px solid black; padding: 8px;"><strong>Revisión Evaluación y Aprobación</strong></td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Solicitado por</td>
            <td style="border: 1px solid black; padding: 8px;">{control.Nombre_Completo}</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px;">Aprobada por</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
            <td style="border: 1px solid black; padding: 8px;">Fecha</td>
            <td style="border: 1px solid black; padding: 8px;">TBD</td>
        </tr>
    </table>
</body>
</html>

        
        '''
        # Adjunta el contenido HTML al correo electrónico
        correo.attach_alternative(html_content, "text/html")

        # Envía el correo
        correo.send()

# Llamar a la función enviar_correo_control_de_cambios con el admin de Django