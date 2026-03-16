# Data Engineering Learning

Repositorio donde documento mi proceso de aprendizaje y práctica orientado al área de **Data Engineering**.

La idea de este repositorio es ir construyendo distintos ejercicios y mini proyectos relacionados con el trabajo con datos, incluyendo consultas SQL, procesamiento de datos con Python y construcción de pipelines simples.

Muchos de los ejercicios simulan pequeños escenarios que se pueden encontrar en entornos reales de análisis o ingeniería de datos.

## Tecnologías utilizadas

Este repositorio utiliza herramientas muy comunes dentro del ecosistema de datos.

### Python

Python se utiliza para implementar procesos de **ETL (Extract, Transform, Load)** dentro de los pipelines de datos.

En este proyecto Python permite:

- leer datasets desde archivos CSV
- limpiar y transformar datos
- automatizar la carga de información hacia una base de datos
- preparar datos para su posterior análisis

Se utilizan principalmente las librerías:

- `pandas` para manipulación de datos
- `psycopg2` para conectarse a PostgreSQL

Python es una de las herramientas más utilizadas en **Data Engineering** debido a su flexibilidad para trabajar con diferentes fuentes de datos.

### PostgreSQL

PostgreSQL se utiliza como motor de base de datos para almacenar y consultar la información.

Se eligió porque:

- es uno de los motores relacionales más utilizados en entornos profesionales
- permite realizar consultas analíticas complejas
- es ampliamente usado en pipelines de datos y sistemas analíticos
- es open source y muy robusto

En este repositorio se utiliza PostgreSQL para almacenar los datos del pipeline y ejecutar consultas SQL analíticas.

### DBeaver

DBeaver se utiliza como cliente de base de datos para interactuar con PostgreSQL.

Permite:

- ejecutar consultas SQL
- explorar tablas
- visualizar resultados
- administrar la base de datos

Es una herramienta bastante común entre **analistas de datos, BI developers y data engineers**.

## Arquitectura del pipeline

El proyecto implementa un pipeline de datos simple con el siguiente flujo:

CSV > Python (con librería pandas) > PostgreSQL > SQL Analytics

### Etapas del pipeline

**1. Extract**

Se carga un dataset de ventas desde un archivo CSV utilizando Python.

**2. Transform**

Los datos son limpiados y normalizados utilizando `pandas` para asegurar consistencia en las columnas.

**3. Load**

Los datos transformados se insertan en una tabla de PostgreSQL utilizando la librería `psycopg2`.

**4. Analyze**

Finalmente se ejecutan consultas SQL para generar insights a partir de los datos almacenados.

## Proyecto: Pipeline de Ventas

Como primer mini proyecto se construyó un pipeline simple para analizar un dataset de ventas.

El objetivo es simular un flujo básico de datos similar al que podría existir en un sistema real de análisis.

El proceso consiste en:

1. Cargar datos desde un archivo CSV
2. Limpiar los datos utilizando Python
3. Insertar los datos en PostgreSQL
4. Ejecutar consultas SQL para analizarlos

El dataset contiene las siguientes columnas:

- cliente
- producto
- precio
- region
- fecha

## Consultas SQL realizadas

Las consultas incluidas en el proyecto abarcan distintos tipos de análisis:

- exploración de datos
- agregaciones con `GROUP BY`
- análisis de ventas
- análisis por región
- análisis de clientes
- métricas de negocio

Algunos ejemplos de análisis realizados:

- ventas totales por región
- productos más vendidos
- clientes que más gastan
- ticket promedio de compra
- evolución de ventas en el tiempo

Todas las consultas se encuentran en: sql/ventas_queries.sql

## Insights del análisis de ventas

A partir de las consultas SQL realizadas sobre la tabla `ventas_pipeline` se pueden obtener distintos insights sobre el comportamiento de las ventas.

### 1. Distribución de ingresos por región

Este análisis permite identificar qué regiones generan mayor volumen de ingresos.

```sql
SELECT region, SUM(precio) AS total_ventas
FROM ventas_pipeline
GROUP BY region
ORDER BY total_ventas DESC;


