from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+14155238886" 
CONTENT_SID = os.getenv("TWILIO_CONTENT_SID")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_message(to: str, token: str) -> str | None:
    """
    Envia mensagem de confirmação via WhatsApp.
    Retorna message.sid se enviado com sucesso, ou None se falhar.
    """
    try:
        message = client.messages.create(
            from_=FROM_NUMBER,
            content_sid=CONTENT_SID,
            content_variables=f'{{"1":"{token}"}}',
            to=f"whatsapp:{to}"
        )
        return message.sid
    except Exception as e:
        print(f"[ERRO WHATSAPP] Falha ao enviar para {to}: {e}")
        return None
