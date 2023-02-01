from mailjet_rest import Client
import os

class Mailjet(object):

    @classmethod
    def send_email(cls, data):
        API_KEY = os.environ.get('DJANGO_SMTP_USER', None)
        API_SECRET = os.environ.get('DJANGO_SMTP_PASS', None)

        if API_SECRET is not None:
            mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

            mailjet_data = {'Messages': [{
                "From": {"Email": data['sender']},
                "To": [{"Email": data['receiver']}],
                "Subject": data['subject'],
                "TextPart": data['message_txt'],
                "HTMLPart": data['message_html']}]
            }

            result = mailjet.send.create(data=mailjet_data)

            return True if result.status_code == 200 else False
