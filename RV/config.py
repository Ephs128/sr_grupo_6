import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definir rutas específicas basadas en la ruta base
DATA_DIR = os.path.join(BASE_DIR, 'data')
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')
