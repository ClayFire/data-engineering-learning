import pandas as pd
import psycopg2

# Leer CSV
df = pd.read_csv("projects/ventas_pipeline.csv", sep=",", engine="python")

# corregir problema de columnas pegadas
df = df.iloc[:,0].str.split(",", expand=True)

df.columns = ["cliente","producto","precio","region","fecha"]

print("Archivo CSV leído correctamente")
print(df.head())


print("Columnas detectadas:")
print(df.columns.tolist())

# Normalizar nombres de columnas
df.columns = df.columns.str.lower().str.strip()

print("Archivo CSV leído correctamente")

# Conectarse a PostgreSQL.
# Permite que Python hable con PostgreSQL.
conexion = psycopg2.connect(
    host="localhost",
    database="data_learning",
    user="postgres",
    password="1234"
)

cursor = conexion.cursor()

print("Conexión a PostgreSQL exitosa")

# Insertar los datos en la tabla.
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO ventas_pipeline (cliente, producto, precio, region, fecha) VALUES (%s, %s, %s, %s, %s)",
        (row["cliente"], row["producto"], row["precio"], row["region"], row["fecha"])
    )

# Guardar cambios.
conexion.commit()

print("Datos cargados correctamente")

cursor.close()
conexion.close()
