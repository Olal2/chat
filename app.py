from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from pyngrok import ngrok, conf
#openai API
openai.api_key = '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'
#ngrok token
conf.get_default().auth_token = "2wMwvJ4Lm4PRt593cv9uGDFJ6DM_4gjTKXqLM3i9rDvUEJnec"

app = Flask(__name__)
conversaciones = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    from_number = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip()

    if from_number not in conversaciones:
        conversaciones[from_number] = [{"role": "system", "content": "Eres Olal, un asistente amigable y humano en WhatsApp."}]

    conversaciones[from_number].append({"role": "user", "content": incoming_msg})
    respuesta_llm = obtener_respuesta_openai(conversaciones[from_number])

    conversaciones[from_number].append({"role": "assistant", "content": respuesta_llm})

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respuesta_llm)
    return str(resp)

def obtener_respuesta_openai(historial):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=historial
        )
        return respuesta.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Lo siento, hubo un problema procesando tu solicitud."

@app.route('/')
def index():
    return "Bot de WhatsApp con Flask y OpenAI"

if __name__ == '__main__':
    app.run()