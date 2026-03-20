import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# 1. Cargar las variables de seguridad desde el archivo .env
load_dotenv()

# ==========================================
# FASE 1: EXTRACT & TRANSFORM (Transformación)
# ==========================================
print("Iniciando extracción y transformación de datos...")

# Leer CSV
df = pd.read_csv(r"C:\Users\USUARIO\Desktop\data-engineering-learning\data\ventas_pipeline.csv", sep=",", engine="python") 

# Corregir problema de columnas pegadas
df = df.iloc[:,0].str.split(",", expand=True)

# Asignar y normalizar nombres de columnas
df.columns = ["cliente", "producto", "precio", "region", "fecha"]
df.columns = df.columns.str.lower().str.strip()

print("Archivo CSV leído y transformado correctamente.")
print(df.head())

# ==========================================
# FASE 2: LOAD (Carga a PostgreSQL)
# ==========================================
conexion = None # Inicializamos la variable por si falla la conexión

try:
    # 2. Conectarse a PostgreSQL usando las variables de entorno (seguridad)
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    cursor = conexion.cursor()
    print("Conexión a PostgreSQL exitosa y segura.")

    # Insertar los datos en la tabla con lógica UPSERT (Idempotencia)
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO ventas_pipeline (cliente, producto, precio, region, fecha) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (cliente, producto, fecha) 
            DO UPDATE SET 
                precio = EXCLUDED.precio,
                region = EXCLUDED.region;
            """,
            (row["cliente"], row["producto"], row["precio"], row["region"], row["fecha"])
        )

    # Guardar cambios.
    conexion.commit()
    print("Datos cargados correctamente a la base de datos.")

except Exception as e:
    # 3. Manejo de errores: Si algo falla, lo reportamos sin "explotar"
    print(f"Error crítico durante la conexión o carga de datos: {e}")
    if conexion:
        conexion.rollback() # Deshace cualquier inserción a medias para no corromper la base de datos

finally:
    # 4. Limpieza: Esto asegura que la conexión SIEMPRE se cierre, haya error o no.
    if conexion:
        cursor.close()
        conexion.close()
        print("Conexión a la base de datos cerrada.")