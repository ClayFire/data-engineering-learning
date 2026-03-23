import pandas as pd
import psycopg2
import os
import logging
from dotenv import load_dotenv

# 1. Configuración del sistema de Logs (Bitácora)
logging.basicConfig(
    filename='etl_ejecucion.log',      # Nombre del archivo donde se guardará el historial
    level=logging.INFO,                # Nivel de detalle que queremos registrar
    format='%(asctime)s - [%(levelname)s] - %(message)s', # Formato: Fecha - Nivel - Mensaje
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Ahora usamos logging en lugar de print
logging.info("Iniciando extracción y transformación de datos...")

load_dotenv()

try:
    # Leer CSV
    df = pd.read_csv(r"C:\Users\USUARIO\Desktop\data-engineering-learning\data\ventas_pipeline.csv", sep=",", engine="python")
    
    # --- DEBUGGING Y TRANSFORMACIÓN ---
    # 1. Escribir en el log EXACTAMENTE cómo lee Python las columnas
    logging.info(f"Columnas originales detectadas: {df.columns.tolist()}")
    
    # 2. Limpiar espacios y forzar minúsculas para evitar errores (Data Cleansing)
    df.columns = df.columns.str.strip().str.lower()
    
    logging.info(f"Archivo CSV listo. Filas: {len(df)}. Columnas finales: {df.columns.tolist()}")

    # Conexión a la Base de Datos
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conexion.cursor()
    logging.info("Conexión a PostgreSQL exitosa y segura.")

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
    
    conexion.commit()
    logging.info("Datos cargados correctamente a la base de datos sin duplicados.")

except Exception as e:
    # Si hay un error, lo guardamos como ERROR CRÍTICO en el log
    logging.error(f"Error crítico durante el proceso: {e}")
    if 'conexion' in locals() and conexion:
        conexion.rollback()
        logging.warning("Se realizó un rollback de la transacción para proteger la base de datos.")

finally:
    if 'conexion' in locals() and conexion:
        cursor.close()
        conexion.close()
        logging.info("Conexión a la base de datos cerrada limpiamente.\n" + "-"*50)