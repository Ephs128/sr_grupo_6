import os
import numpy as np
from RV.preprocessing.PreProcesamiento import extraer_mfcc, rellenar_caracteristicas
from RV.dir import CSV_DIR, CSV_ACC, SAMPLES
def crear_data_set():
    print("creando dataset...")

    features_list_dir = []
    labels_list_dir = []
    features_list_acc = []
    labels_list_acc = []
    max_timesteps = 0
    for folder_name_0 in os.listdir(SAMPLES):
        folder_path_0 = os.path.join(SAMPLES, folder_name_0)
        for folder_name in os.listdir(folder_path_0):
            folder_path = os.path.join(folder_path_0, folder_name)
            if os.path.isdir(folder_path):
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.wav'):
                        file_path = os.path.join(folder_path, file_name)
                        features = extraer_mfcc(file_path)
                        if folder_name_0 == "direccion":
                            features_list_dir.append(features)
                            labels_list_dir.append(folder_name)
                        else:
                            features_list_acc.append(features)
                            labels_list_acc.append(folder_name)
                        if len(features) > max_timesteps:
                            max_timesteps = len(features)

    # Convertir las listas de características y etiquetas a un DataFrame de pandas
    padded_features_dir = rellenar_caracteristicas(features_list_dir, max_timesteps)
    padded_features_acc = rellenar_caracteristicas(features_list_acc, max_timesteps)

    features_array_dir = np.array(padded_features_dir, dtype=object)
    labels_array_dir = np.array(labels_list_dir)

    features_array_acc = np.array(padded_features_acc, dtype=object)
    labels_array_acc = np.array(labels_list_acc)


    np.savez(CSV_DIR, features=features_array_dir, labels=labels_array_dir)
    np.savez(CSV_ACC, features=features_array_acc, labels=labels_array_acc)
    print("dataset creado...")
