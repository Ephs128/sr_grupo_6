import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from RV.preprocessing.PreProcesamiento import rellenar_caracteristicas

class RnnRecognizer(object):
    TRADUCTOR_DIRECCION = {
        0: "arriba",
        1: "abajo",
        2: "left",
        3: "derecha",
    }

    TRADUCTOR_ACCION = {
        0: "mover",
        1: "empujar"
    }

    def __init__(self, ruta_datos_dir, ruta_datos_acc):
        X1, y1 = self.__recuperar_datos(ruta_datos_dir, self.TRADUCTOR_DIRECCION)
        X2, y2 = self.__recuperar_datos(ruta_datos_acc, self.TRADUCTOR_ACCION)
        self.__modelo_dir = self.__crear_modelo(X1, y1)
        self.__modelo_acc = self.__crear_modelo(X2, y2)
        self.__max_tam_sec_dir = len(X1[0])
        self.__max_tam_sec_acc = len(X2[0])

    def __crear_modelo(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo = Sequential([
            Input(shape=(X_train.shape[1], X_train.shape[2])),
            LSTM(units=128),
            Dense(len(np.unique(y)), activation="softmax")
        ])

        modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        modelo.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
        return modelo

    def __recuperar_datos(self, ruta_datos, traductor):
        traductor_invertido = {v: k for (k, v) in traductor.items()}
        datos = np.load(ruta_datos, allow_pickle=True)
        X = np.array(datos['features'], dtype=np.float32)
        y = datos['labels']
        y = np.array([traductor_invertido[dat] for dat in y], dtype=np.float32)
        return X, y

    def reconocer_palabra_accion(self, mfccs):
        tam_segments_mfccs = len(mfccs)
        if tam_segments_mfccs > self.__max_tam_sec_acc:
            raise IndexError("Mucho ruido, baje la sensibilidad")
        X = rellenar_caracteristicas([mfccs], self.__max_tam_sec_acc)
        X = np.array(X, dtype=np.float32)
        prediccion = self.__modelo_acc.predict(X)
        indice = np.argmax(prediccion)
        return self.TRADUCTOR_ACCION[indice]

    def reconocer_palabra_direccion(self, mfccs):
        tam_segments_mfccs = len(mfccs)
        if tam_segments_mfccs>self.__max_tam_sec_dir:
            raise IndexError()
        X = rellenar_caracteristicas([mfccs], self.__max_tam_sec_dir)
        X = np.array(X, dtype=np.float32)
        prediccion = self.__modelo_dir.predict(X)
        indice = np.argmax(prediccion)
        return self.TRADUCTOR_DIRECCION[indice]


