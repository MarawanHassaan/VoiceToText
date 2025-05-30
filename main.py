import asyncio
import websockets
import speech_recognition as sr
import json  # For encoding messages as JSON

async def speech_recognition(websocket, path):
    recognizer = sr.Recognizer()
    keyword = "hello"
    print("Server ready, waiting for client command...")

    # Await a message to start listening
    start_message = await websocket.recv()
    if start_message == "start_listening":
        # Send a structured message indicating that this should be spoken
        await websocket.send(json.dumps({"text": "Listening...", "speak": True}))
        with sr.Microphone() as source:
            print("Microphone is ready, adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while True:
                print("Listening for audio...")
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio).lower()
                    # print(f"Recognized text: {text}")
                    # Send recognized text normally, not to be spoken
                    # await websocket.send(json.dumps({"text": text, "speak": False}))

                    if keyword in text:
                        print(f"Keyword '{keyword}' detected.")

                        await websocket.send(json.dumps({"text": "How may I help you today", "speak": True}))
                        await asyncio.sleep(1)
                        audio = recognizer.listen(source)
                        text = recognizer.recognize_google(audio).lower()
                        print(text)
                        await websocket.send(json.dumps({"text": "Shut up", "speak": True}))
                        await asyncio.sleep(0.1)
                        response_text = "LLM output"
                        # Send LLM output with indication to speak it
                        await websocket.send(json.dumps({"text": response_text, "speak": True}))
                        await asyncio.sleep(1)
                        break
                except sr.UnknownValueError:
                    await websocket.send(json.dumps({"text": "Could not understand audio", "speak": False}))
                except sr.RequestError as e:
                    await websocket.send(json.dumps({"text": f"Request failed: {str(e)}", "speak": False}))

start_server = websockets.serve(speech_recognition, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()