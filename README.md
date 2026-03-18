# Data Engineering Learning

Repositorio donde documento mi proceso de aprendizaje orientado al área de **Data Engineering**.

Este repositorio reúne ejercicios y mini proyectos enfocados en el trabajo con datos, incluyendo consultas SQL, procesamiento con Python y construcción de pipelines simples.

Los ejercicios están diseñados para simular escenarios reales que pueden encontrarse en entornos de análisis e ingeniería de datos.

---

## Tecnologías utilizadas

Este repositorio utiliza herramientas ampliamente utilizadas en el ecosistema de datos.

### Python

Python se utiliza para implementar procesos de **ETL (Extract, Transform, Load)** dentro de los pipelines.

En este proyecto permite:

- leer datasets desde archivos CSV
- limpiar y transformar datos
- automatizar la carga hacia una base de datos
- preparar datos para análisis posterior

Librerías utilizadas:

- `pandas` para manipulación de datos
- `psycopg2` para conexión con PostgreSQL

---

### PostgreSQL

PostgreSQL se utiliza como sistema de almacenamiento y consulta de datos.

Se eligió porque:

- es ampliamente utilizado en entornos profesionales
- permite consultas analíticas complejas
- es robusto y open source

En este proyecto actúa como base de datos del pipeline y del modelo analítico.

---

### DBeaver

DBeaver se utiliza como cliente para interactuar con la base de datos.

Permite:

- ejecutar consultas SQL
- explorar tablas
- visualizar resultados

---

## Arquitectura del pipeline

El pipeline implementado sigue un flujo simple:

CSV > Python (librería pandas) > PostgreSQL > SQL Analytics


### Etapas

**1. Extract**  
Carga de datos desde un archivo CSV.

**2. Transform**  
Limpieza y normalización de datos con `pandas`.

**3. Load**  
Inserción de datos en PostgreSQL mediante `psycopg2`.

**4. Analyze**  
Ejecución de consultas SQL para obtener insights.

---

## Proyecto: Pipeline de Ventas

Se construyó un pipeline simple utilizando un dataset de ventas para simular un flujo real de datos.

El proceso consiste en:

1. cargar datos desde CSV  
2. transformarlos con Python  
3. almacenarlos en PostgreSQL (`ventas_pipeline`)  
4. analizarlos con SQL  

### Dataset

Columnas utilizadas:

- cliente  
- producto  
- precio  
- region  
- fecha  

---

## Consultas SQL realizadas

Las consultas abarcan distintos tipos de análisis:

- exploración de datos  
- agregaciones con `GROUP BY`  
- análisis por región, producto y cliente  
- métricas de negocio  

Archivo:

sql/ventas_queries.sql


---

## Insights del análisis de ventas

A partir de las consultas sobre `ventas_pipeline` se pueden obtener distintos insights.

### Distribución de ingresos por región

Permite identificar qué regiones generan mayor volumen de ingresos.

```sql
SELECT region, SUM(precio) AS total_ventas
FROM ventas_pipeline
GROUP BY region
ORDER BY total_ventas DESC;


---


## Cómo ejecutar el proyecto

1. Clonar el repositorio

git clone https://github.com/tu_usuario/data-engineering-learning.git

2. Instalar dependencias 

pip install pandas psycopg2-binary

3. Crear tabla en PostgreSQL (ejecutar scripts correspondientes)

4. Ejecuta la carga de datos

python python/cargar_ventas_postgres.py


---


## Data Warehouse – Modelo Estrella

Para mejorar el análisis, los datos fueron transformados desde ventas_pipeline a un modelo dimensional tipo estrella.

Este modelo es ampliamente utilizado en Data Warehouses porque:

- optimiza consultas analíticas

- separa métricas de dimensiones

- evita duplicidad de información


---


## Estructura del modelo

Tabla de hechos:

fact_ventas

Contiene la métrica principal (precio) y las claves hacia las dimensiones.


---


## Tablas de dimensiones

dim_cliente

dim_producto

dim_region

dim_fecha

Permiten analizar los datos desde distintas perspectivas.