import librosa
import librosa.display
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy.signal import medfilt
from RV.dir import RECORDED_RAW, RECORDED_PROC
from RV.constants import MFCCS_DIM, THRESHOLD, HOP_LENGHT, SR, MAX_RECORD_DURATION

def extraer_mfcc(ruta_audio):
    y, sr = librosa.load(ruta_audio)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=MFCCS_DIM)
    return mfccs.T  # Transponer para tener frames x n_mfcc

def preprocesar_audio(audio_path):
    audio, sr = librosa.load(audio_path)

    audio = librosa.to_mono(audio)

    audio_normalizado = librosa.util.normalize(audio)

    audio_resampled = librosa.resample(audio_normalizado, orig_sr=librosa.get_samplerate(audio_path), target_sr=SR)

    audio_filtrado = medfilt(audio_resampled, kernel_size=3)

    audio_filtrado = np.int16(audio_filtrado * 32767)
    tramos_activos = librosa.effects.split(audio_filtrado, top_db=THRESHOLD, hop_length=HOP_LENGHT)

    audio_sin_espacios, _ = librosa.effects.trim(audio_filtrado)


    for inicio, fin in tramos_activos:
        audio_sin_espacios = []
        audio_sin_espacios.extend(audio_filtrado[inicio:fin])
        sf.write(RECORDED_PROC, audio_sin_espacios, sr)
    print(f"tamaño de segmentos { len(tramos_activos) }")
    audio_sin_espacios = np.array(audio_sin_espacios)


def grabar_audio(duracion, nombre):
    print("Grabando...")
    audio = sd.rec(int(duracion * SR), samplerate=SR, channels=1)
    sd.wait()  # Espera a que la grabación termine
    print("Grabación completada.")
    sf.write(nombre, audio, SR)
    print(f"Archivo guardado como {nombre}")

def grabar_nuevo_audio():
    grabar_audio(MAX_RECORD_DURATION, nombre=RECORDED_RAW)
    print("preprocesando...")
    preprocesar_audio(RECORDED_RAW)
    print("preprocesamiento completado.")
    print(f"Archivo guardado como { RECORDED_RAW }")