import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Cargar variables de entorno
load_dotenv()

print("Conectando al Data Warehouse para generar el reporte gerencial...")

try:
    # 1. Conexión moderna usando SQLAlchemy Engine
    # Formato de conexión: postgresql+psycopg2://usuario:password@host:puerto/base_de_datos
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    cadena_conexion = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(cadena_conexion)

    # 2. La consulta maestra (MoM)
    query_mom = """
    WITH VentasMensuales AS (
        SELECT 
            EXTRACT(YEAR FROM d.fecha) AS anio,
            EXTRACT(MONTH FROM d.fecha) AS mes,
            SUM(f.precio) AS ingresos_actuales
        FROM fact_ventas f
        JOIN dim_fecha d ON f.fecha_id = d.fecha_id
        GROUP BY 
            EXTRACT(YEAR FROM d.fecha),
            EXTRACT(MONTH FROM d.fecha)
    )
    SELECT 
        anio,
        mes,
        ingresos_actuales,
        LAG(ingresos_actuales) OVER (ORDER BY anio, mes) AS ingresos_mes_anterior,
        ROUND(
            ( (ingresos_actuales - LAG(ingresos_actuales) OVER (ORDER BY anio, mes))::numeric * 100.0 ) / 
            LAG(ingresos_actuales) OVER (ORDER BY anio, mes)::numeric
        , 2) AS porcentaje_crecimiento
    FROM VentasMensuales
    ORDER BY anio, mes;
    """

    # 3. Ejecutar la consulta usando el Motor (sin advertencias)
    print("Ejecutando consulta analítica avanzada (Window Functions)...")
    df_reporte = pd.read_sql_query(query_mom, engine)

    # 4. Exportar a CSV
    ruta_salida = os.path.join(os.path.dirname(__file__), '..', 'data', 'reporte_crecimiento_mom.csv')
    df_reporte.to_csv(ruta_salida, index=False, sep=";") 

    print(f"¡Éxito! Reporte gerencial generado correctamente en: {ruta_salida}")
    print("-" * 50)
    print(df_reporte)

except Exception as e:
    print(f"Ocurrió un error al generar el reporte: {e}")