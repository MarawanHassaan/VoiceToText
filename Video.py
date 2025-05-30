from moviepy.editor import VideoClip, AudioFileClip
import math
import librosa
import numpy as np
from gtts import gTTS

def generate_equalizer_video(text, fps=25, sample_rate=44100):

    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty")
    audio_data = text_to_wav(text, sample_rate)

    # Extract features from audio
    mel_spectrogram = extract_mel_spectrogram(audio_data, sample_rate)
    frequencies = librosa.core.mel_frequencies(n_mels=128, fmax=sample_rate // 2)

    def make_frame(t):

        index = int(t * fps)
        if index >= len(mel_spectrogram):
            return np.zeros((256, 720, 3), dtype=np.uint8)
        spectrogram_db = librosa.power_to_db(mel_spectrogram[:, index])

        frame = np.zeros((256, 720, 3), dtype=np.uint8)
        frame.fill(20)
        bar_width = 5
        bar_gap = 2
        for i, freq in enumerate(frequencies):
            bar_height = int(max(0, spectrogram_db[i]) * 255 / 80)
            y_start = 256 - bar_height
            x_start = i * (bar_width + bar_gap)
            frame[y_start:, x_start:x_start + bar_width] = (255, 255, 0)  # Red color

        return frame

    duration = len(audio_data) / sample_rate
    video_clip = VideoClip(make_frame, duration=duration)
    audio_clip = AudioFileClip("temp.wav")
    final_clip = video_clip.set_audio(audio_clip)
    return final_clip


def text_to_wav(text, sample_rate):

    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("temp.wav")

    audio_data, _ = librosa.load("temp.wav", sr=sample_rate)

    # Remove temporary audio file
    # import os
    # os.remove("temp.wav")

    return audio_data


def extract_mel_spectrogram(audio_data, sample_rate):
    melspectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128)
    return melspectrogram

def main_video(text):
    video = generate_equalizer_video(text)
    video.write_videofile("equalizer.mp4", fps=25)

    print("Equalizer video generated successfully!")
