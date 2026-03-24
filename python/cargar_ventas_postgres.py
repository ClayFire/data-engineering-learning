import pandas as pd
import psycopg2
import os
import logging
from dotenv import load_dotenv

# 1. Configuración del sistema de Logs
logging.basicConfig(
    filename='etl_ejecucion.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Iniciando extracción y transformación de datos...")

load_dotenv()

try:
    # Leer CSV
    df = pd.read_csv(r"C:\Users\USUARIO\Desktop\data-engineering-learning\data\ventas_pipeline.csv", sep=",", engine="python")
    
    # --- TRANSFORMACIÓN Y LIMPIEZA ---
    df.columns = df.columns.str.strip().str.lower()
    
    # --- DATA QUALITY (ESCUDO DE CALIDAD) ---
    filas_iniciales = len(df)
    
    # El Escudo: Sobrescribimos el DataFrame conservando SOLO las filas con precio > 0
    df = df[df['precio'] > 0]
    
    filas_eliminadas = filas_iniciales - len(df)
    
    if filas_eliminadas > 0:
        logging.warning(f"ESCUDO ACTIVO: Se bloquearon y eliminaron {filas_eliminadas} fila(s) por tener un precio inválido (negativo o cero).")
    else:
        logging.info("Control de Calidad superado: Todos los precios son correctos (mayores a 0).")

    logging.info(f"Archivo CSV listo para cargar a la base de datos. Filas válidas: {len(df)}")

    # --- CARGA A BASE DE DATOS ---
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conexion.cursor()
    logging.info("Conexión a PostgreSQL exitosa y segura.")

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
    logging.error(f"Error crítico durante el proceso: {e}")
    if 'conexion' in locals() and conexion:
        conexion.rollback()
        logging.warning("Se realizó un rollback de la transacción para proteger la base de datos.")

finally:
    if 'conexion' in locals() and conexion:
        cursor.close()
        conexion.close()
        logging.info("Conexión a la base de datos cerrada limpiamente.\n" + "-"*50)