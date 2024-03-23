from django.core.mail import send_mail

subject = 'Asunto del correo'
message = 'Contenido del correo'
from_email = 'grullona283@gmail.com'
recipient_list = ['jgrullon@napdelcaribe.com.do']

send_mail(subject, message, from_email, recipient_list)
