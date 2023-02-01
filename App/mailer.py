from App.mailjet import Mailjet
from elcorredorprototipo import settings
import os

class Mailer(object):

    @classmethod
    def send_reset_password_mail(cls, user):
        base_url = settings.PRODUCTION_URL if os.environ.get('DJANGO_ENV', '') == 'Production' else settings.DEVELOPMENT_URL
        token = user.verifications.password_reset_token
        data = {
            'sender': settings.DEFAULT_FROM_EMAIL,
            'receiver': user.email,
            'subject': 'Solicitud restablecimiento de contraseña',
            'message_txt': f'Se ha solicitado el reinicio de la contraseña para el usuario con email {user.email} \nPara establecer una nueva contraseña haz click en el enlace de abajo:\n{base_url}/accounts/password_reset/{token}/',
            'message_html': f'<p>Se ha solicitado el reinicio de la contraseña para el usuario con email {user.email}<br/>Para establecer una nueva contraseña haz click en el enlace de abajo:<br/><a href="{base_url}/accounts/password_reset/{token}/">{base_url}/accounts/password_reset/{token}/</a></p>'
        }

        Mailjet.send_email(data)


    @classmethod
    def send_email_verification_mail(cls, user):
        base_url = settings.PRODUCTION_URL if os.environ.get('DJANGO_ENV', '') == 'Production' else settings.DEVELOPMENT_URL
        token = user.verifications.email_verification_token
        data = {
            'sender': settings.DEFAULT_FROM_EMAIL,
            'receiver': user.email,
            'subject': 'Verifica tu email',
            'message_txt': f'Necesitas verificar que el email {user.email} te pertenece\nPara verificar tu email haz click en el enlace de abajo: \n{base_url}/accounts/verify_email/{token}/',
            'message_html': f'<p>Necesitas verificar que el email {user.email} te pertenece<br/>Para verificar tu email haz click en el enlace de abajo:<br/><a href="{base_url}/accounts/verify_email/{token}/">{base_url}/accounts/verify_email/{token}/</a></p>'
        }

        Mailjet.send_email(data)


    @classmethod
    def send_email_update_mail(cls, user, new_email):
        base_url = settings.PRODUCTION_URL if os.environ.get('DJANGO_ENV', '') == 'Production' else settings.DEVELOPMENT_URL
        token = user.verifications.email_verification_token
        data = {
            'sender': settings.DEFAULT_FROM_EMAIL,
            'receiver': new_email,
            'subject': 'Verifica tu cambio de email',
            'message_txt': f'Para cambiar del email {user.email} al email {new_email} necesitas verificar que el nuevo email te pertenece\nPara verificar tu email haz click en el enlace de abajo: \n{base_url}/accounts/verify_email/{token}/',
            'message_html': f'<p>Para cambiar del email {user.email} al email {new_email} necesitas verificar que el nuevo email te pertenece<br/>Para verificar tu email haz click en el enlace de abajo:<br/><a href="{base_url}/accounts/verify_email/{token}/">{base_url}/accounts/verify_email/{token}/</a></p>'
        }

        Mailjet.send_email(data)


    @classmethod
    def send_email_create_property(cls, new_property):
        base_url = settings.PRODUCTION_URL if os.environ.get('DJANGO_ENV', '') == 'Production' else settings.DEVELOPMENT_URL
        data = {
            'sender': 'contratos@elcorredor.org',
            'receiver': new_property.user.email,
            'subject': 'Condiciones para publicar tu propiedad',
            'message_txt': f'¡Gracias por tu interés en publicar la venta de tu propiedad con referencia catastral {new_property.catastral_reference} en nuestro sitio web!\nNuestro sitio web cobra una comisión del 10% por cada venta que se realice.\nTu propiedad no aparecerá como publicada en nuestra web hasta que no aceptes esta condición y nos envíes los documentos que acrediten que tú eres el propietario de la propiedad.\nSi estás de acuerdo con nuestras condiciones, por favor, contesta a este email adjuntando una copia de tu DNI y la escritura o copia simple del registro de la propiedad donde se pueda ver que eres tú el propietario de la propiedad.\nAl contestar a este email y enviarnos la documentación aceptas los términos y condiciones de venta mencionados anteriormente.\nUna vez revisada y comprobada la documentación enviada, tu propiedad aparecerá publicada en nuestro sitio web y cualquier usuario interesado podrá contactarte para negociar el acuerdo de compraventa',
            'message_html': f'<p>¡Gracias por tu interés en publicar la venta de tu propiedad con referencia catastral {new_property.catastral_reference} en nuestro sitio web!<br/>Nuestro sitio web cobra una comisión del 10% por cada venta que se realice.<br/>Tu propiedad no aparecerá como publicada en nuestra web hasta que no aceptes esta condición y nos envíes los documentos que acrediten que tú eres el propietario de la propiedad.<br/>Si estás de acuerdo con nuestras condiciones, por favor, contesta a este email adjuntando una copia de tu DNI y la escritura o copia simple del registro de la propiedad donde se pueda ver que eres tú el propietario de la propiedad.<br/>Al contestar a este email y enviarnos la documentación aceptas los términos y condiciones de venta mencionados anteriormente.<br/>Una vez revisada y comprobada la documentación enviada, tu propiedad aparecerá publicada en nuestro sitio web y cualquier usuario interesado podrá contactarte para negociar el acuerdo de compraventa</p>'
        }

        Mailjet.send_email(data)


    @classmethod
    def send_email_property_contact(cls, user, property, message):
        base_url = settings.PRODUCTION_URL if os.environ.get('DJANGO_ENV', '') == 'Production' else settings.DEVELOPMENT_URL
        data = {
            'sender': settings.DEFAULT_FROM_EMAIL,
            'receiver': property.user.email,
            'subject': 'Alquien está interesado en tu propiedad',
            'message_txt': f'¡Enhorabuena!\nEl usuario con dirección de correo electrónico {user.email} está interesado en tu propiedad con referencia catastral {property.catastral_reference}\nTe ha enviado el siguiente mensaje:\n{message}\nPara contestarle, no respondas a este email, mándale un mensaje a su dirección de correo electrónico.',
            'message_html': f'<p>¡Enhorabuena!<br/>El usuario con dirección de correo electrónico {user.email} está interesado en tu propiedad con referencia catastral {property.catastral_reference}<br/>Te ha enviado el siguiente mensaje:<br/>{message}<br/>Para contestarle, no respondas a este email, mándale un mensaje a su dirección de correo electrónico.</p>'
        }

        Mailjet.send_email(data)
