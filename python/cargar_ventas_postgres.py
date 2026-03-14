import pandas as pd
import psycopg2

# Leer el archivo CSV.
# Aquí pandas carga el CSV como una tabla en memoria.
df = pd.read_csv("../projects/ventas_pipeline.csv")

print("Archivo CSV leído correctamente")

# Conectarse a PostgreSQL.
# Permite que Python hable con PostgreSQL.
conexion = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234"
)

cursor = conexion.cursor()

print("Conexión a PostgreSQL exitosa")

# Insertar los datos en la tabla.
for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO ventas_pipeline (cliente, producto, precio, region, fecha)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (row["cliente"], row["producto"], row["precio"], row["region"], row["fecha"])
    )

# Guardar cambios.
conexion.commit()

print("Datos cargados correctamente")

cursor.close()
conexion.close()
