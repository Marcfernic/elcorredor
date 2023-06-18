from mailjet_rest import Client

class Mailjet(object):

    @classmethod
    def send_email(cls, data):
        API_KEY = "8e1f9bd3d15d633cc707c17672abcd57"  # Reemplaza "TU_API_KEY" con el valor real de tu clave de API
        API_SECRET = "304fe9d954b204e1ad9329cd72c6c5aa"  # Reemplaza "TU_API_SECRET" con el valor real de tu secreto de API

        mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')

        mailjet_data = {
            'Messages': [{
                "From": {"Email": data['sender']},
                "To": [{"Email": data['receiver']}],
                "Subject": data['subject'],
                "TextPart": data['message_txt'],
                "HTMLPart": data['message_html']
            }]
        }

        result = mailjet.send.create(data=mailjet_data)

        return True if result.status_code == 200 else False