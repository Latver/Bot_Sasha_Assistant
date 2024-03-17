import torch, pyaudio, threading
import numpy as np
import re
from num2words import num2words

sample_rate = 48000
speaker = 'xenia'

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language='ru', speaker='v3_1_ru')
device = torch.device('cpu')
model.to(device)

def preprocess_numbers(text):
    text = re.sub(r'\d+', lambda m: num2words(int(m.group(0)), lang='ru'), text)

    special_characters = {'%': 'процент', '$': 'доллар', '#': 'решетка', '@': 'собака', '&': 'амперсанд', '№': 'номер', '*': '',
    "a": "а", "b": "б", "c": "ц", "d": "д", "e": "е", "f": "ф", "g": "г", "h": "х", "i": "и", "j": "джей", 
    "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "w": "в", "x": "икс", "y": "ай", "z": "з",
    "A": "А", "B": "Б", "C": "Ц", "D": "Д", "E": "Е", "F": "Ф", "G": "Г", "H": "Х", "I": "И", "J": "Джей", 
    "K": "К", "L": "Л", "M": "М", "N": "Н", "O": "О", "P": "П", "Q": "К", "R": "Р", "S": "С", "T": "Т", "U": "У", "V": "В", "W": "В", "X": "Икс", "Y": "Ай", "Z": "З"}

    for char, replacement in special_characters.items():
        text = text.replace(char, replacement)

    return text

def split_text(text, max_length=900):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_length:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# def va_speak(user_voice):
#     threading.Thread(target=threaded_va_speak, args=(user_voice,)).start()

def va_speak(user_voice):
    chunks = split_text(user_voice)
    for chunk in chunks:
        chunk = preprocess_numbers(chunk)
        audio = model.apply_tts(text=chunk, speaker=speaker, sample_rate=sample_rate)

        audio_np = audio.numpy()

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(audio_np.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()

def stop_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.stop_stream()
    stream.close()
    p.terminate()

def pause_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.pause()

def unpause_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
    stream.unpause()