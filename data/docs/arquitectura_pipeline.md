# Arquitectura del Pipeline de Ventas

## Descripción

Este proyecto implementa un pipeline de datos simple para analizar ventas utilizando Python, PostgreSQL y SQL.

El objetivo es transformar datos de ventas en insights que permitan entender el comportamiento de clientes, productos y regiones.

## Flujo del pipeline

CSV > Python (librería pandas) > PostgreSQL > SQL Analytics

## 1. Extract
 - Se carga un archivo CSV con registros de ventas.

## 2. Transform
   - Se limpian y normalizan los datos con pandas.

## 3. Load
   - Los datos se insertan en la tabla `ventas_pipeline` en PostgreSQL.

## 4. Analyze
   - Se ejecutan consultas SQL para generar insights de negocio.

## Dataset

El dataset contiene información de ventas con las siguientes columnas:

- cliente
- producto
- precio
- region
- fecha

## Objetivo del análisis

Responder preguntas de negocio como:

- ¿Qué regiones generan más ingresos?
- ¿Qué productos son los más vendidos?
- ¿Qué clientes generan más valor?
- ¿Cómo evolucionan las ventas a lo largo del tiempo?