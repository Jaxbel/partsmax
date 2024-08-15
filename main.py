from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai
import requests
import os

app = FastAPI()

# Configura tu API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/incoming_call", response_class=PlainTextResponse)
async def incoming_call():
    response = VoiceResponse()

    
    response.say("Hello, welcome to partsmax. We are here to help you with your car parts needs.")

    # Primera pregunta con opción de respuesta por voz
    gather = Gather(input='speech', action='/process_response', method='POST')
    gather.say("¿Cómo fue su experiencia con nuestro servicio?")
    response.append(gather)

    return str(response)

@app.post("/process_response", response_class=PlainTextResponse)
async def process_response(RecordingUrl: str = Form(...)):
    response = VoiceResponse()

    # Descarga el audio de la respuesta del usuario
    audio_content = requests.get(RecordingUrl).content

    # Usa OpenAI para transcribir el audio a texto
    transcription = openai.Audio.transcribe("whisper-1", audio_content)

    # Procesa la transcripción con OpenAI para analizar la respuesta
    user_response = transcription['text']
    response.say(f"Usted dijo: {user_response}")

    # Lógica para interpretar la respuesta y continuar el flujo
    if "bien" in user_response.lower():
        response.say("Nos alegra que haya tenido una buena experiencia.")
    else:
        response.say("Lamentamos escuchar eso. Trabajaremos para mejorar.")

    response.hangup()

    return str(response)

if __name__ == "__main__":
    # Corre la aplicación en el puerto 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
