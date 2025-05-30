from pydub import AudioSegment
import speech_recognition as sr
import whisper
import os
import torch
import numpy as np
import time
def stt(audio_model=None,english=True,verbose=False, energy=300, pause=0.8,dynamic_energy=False):
    #there are no english models for large

    audio=record_audio(energy, pause, dynamic_energy)
    text=transcribe_forever(audio, audio_model, english, verbose)
    # print(text)
    return text


def record_audio(energy, pause, dynamic_energy):
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        print("Say something!")
        i = 0
        while True:
            #get and save audio to wav file
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            i+=1
            print("ibtehaj is here", i)
            # if i==100:
            break

        return audio_data

def transcribe_forever(audio, audio_model, english, verbose):
    while True:
        audio_data = audio
        if english:
            result = audio_model.transcribe(audio_data,language='english',fp16=False)
        else:
            result = audio_model.transcribe(audio_data,fp16=False)

        if not verbose:
            predicted_text = result["text"]
            return predicted_text
        else:
            return result
        break
