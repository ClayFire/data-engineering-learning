# Arquitectura del Pipeline de Ventas

Este proyecto implementa un pipeline ETL simple utilizando Python y PostgreSQL.

## Flujo de datos

CSV → Python (pandas) → PostgreSQL → SQL Analytics

## Etapas del pipeline

### 1. Extract
Se carga el dataset de ventas desde un archivo CSV.

### 2. Transform
Se limpian y normalizan los datos usando pandas.

### 3. Load
Los datos transformados se insertan en la tabla `ventas_pipeline` en PostgreSQL.

## Consultas analíticas

El archivo `sql/ventas_queries.sql` contiene consultas para analizar:

- ventas por región
- productos más vendidos
- ranking de clientes
- ventas por mes