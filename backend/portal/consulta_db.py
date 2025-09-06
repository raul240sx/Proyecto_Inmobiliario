import os
import sys
import django
from django.db import connection

# Asegurar que Python pueda importar el proyecto
sys.path.append("/usr/src/app")

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto_inmobiliario.settings")
django.setup()


# Crear carpeta de salida
os.makedirs("/usr/src/app/portal/output", exist_ok=True)
ruta_txt = "/usr/src/app/portal/output/inmuebles_para_arriendo.txt"

with connection.cursor() as cursor:
    cursor.execute('''
        SELECT c.nombre AS comuna, i.nombre AS inmueble, i.descripcion
        FROM portal_inmueble i
        JOIN locations_comuna c ON i.comuna_id = c.id
        WHERE i.arrendado = FALSE
        ORDER BY c.nombre;
    ''')

    resultados = cursor.fetchall()
    columnas = [col[0] for col in cursor.description]

with open(ruta_txt, "w", encoding="utf-8") as f:
    f.write("\t".join(columnas) + "\n")  # encabezados
    for fila in resultados:
        f.write("\t".join(map(str, fila)) + "\n")

print(f"Consulta guardada en {ruta_txt}")