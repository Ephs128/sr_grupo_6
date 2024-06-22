from RV.reconocimiento.RNN.Rnn import RnnRecognizer
from RV.preprocessing.PreProcesamiento import grabar_audio, preprocesar_audio
from RV.dir import CSV_DIR, CSV_ACC, REC_PROC
from RV.constants import MAX_RECORD_DURATION

class Reconocedor(object):

    def __init__(self):
        self.__rnn = RnnRecognizer(CSV_DIR, CSV_ACC)

    def reconocer_voz(self, sensibilidad):
        # grabar la voz
        grabar_audio(MAX_RECORD_DURATION,REC_PROC)
        mfccs = preprocesar_audio(REC_PROC, sensibilidad)

        # etapa de reconocimiento
        comandos = [lambda x: self.__rnn.reconocer_palabra_accion(x), lambda x: self.__rnn.reconocer_palabra_direccion(x)]
        palabras = []
        if len(mfccs) <= 2:
            for i, mfcc in enumerate(mfccs):
                funcion = comandos[i]
                palabra = funcion(mfcc)
                palabras.append(palabra)
            return palabras
        else:
            raise IndexError("La deteccion es muy baja, incremente la sensibilidad")


