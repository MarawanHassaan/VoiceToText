import asyncio
import websockets
import speech_recognition as sr
import json

async def listen_for_speech(recognizer, websocket, listen_once=True):
    """Listen for speech and recognize it using the recognizer."""
    keyword = "hello"
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for audio...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            if keyword in text:
                print(f"Keyword '{keyword}' detected.")
                # await asyncio.sleep(5)
                await send_message(websocket, "How may I help you today?", speak=True)
                await trigger_response(websocket)
                await asyncio.sleep(2)

        except sr.UnknownValueError:
            await send_message(websocket, "Could not understand audio", speak=False)
        except sr.RequestError as e:
            await send_message(websocket, f"Request failed: {str(e)}", speak=False)
        return None

async def trigger_response(websocket):
    """Trigger a response when the keyword is detected."""
    # Listen to the user's question after the prompt


async def send_message(websocket, text, speak):
    """Send a message through the websocket."""
    await websocket.send(json.dumps({"text": text, "speak": speak}))

async def speech_recognition(websocket, path):
    global recognizer  # Make recognizer accessible globally in this module
    recognizer = sr.Recognizer()
    print("Server ready, waiting for client command...")

    # Await a message to start listening
    start_message = await websocket.recv()
    if start_message == "start_listening":
        await send_message(websocket, "Listening...", speak=True)
        while True:
            await listen_for_speech(recognizer, websocket)

start_server = websockets.serve(speech_recognition, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
