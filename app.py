from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# OpenRouter API (usa tu propia clave desde https://openrouter.ai/)
client = OpenAI(
    api_key="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", #API openrouter
    base_url="https://openrouter.ai/api/v1"  # Base URL de OpenRouter
)

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
        respuesta = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",  # ← Puedes cambiarlo por otro modelo de OpenRouter
            messages=historial
        )
        return respuesta.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Lo siento, hubo un problema procesando tu solicitud."

@app.route('/')
def index():
    return "Bot de WhatsApp con Flask y OpenAI (vía OpenRouter)"

if __name__ == '__main__':
    app.run()
