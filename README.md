# Data Engineering End-to-End Pipeline & Data Warehouse

Bienvenido a mi portafolio de Ingeniería de Datos. Este repositorio simula un entorno real de procesamiento de datos, desde la ingesta de archivos planos hasta la construcción de un Data Warehouse modelado para Inteligencia de Negocios (BI).

El objetivo principal de este proyecto es demostrar dominio en la creación de pipelines **robustos, seguros e idempotentes**, orientados a resolver preguntas de negocio.

---

## Tecnologías y Arquitectura

El pipeline sigue un flujo clásico de **ETL (Extract, Transform, Load)**:

**`CSV`** > **`Python (Pandas)`** > **`PostgreSQL`** > **`SQL Analytics`**

* **Python:** Extracción, limpieza y transformación de datos.
* **Pandas:** Manipulación de DataFrames y normalización.
* **PostgreSQL:** Motor de base de datos relacional y Data Warehouse.
* **Psycopg2:** Conector entre Python y la base de datos.
* **Dotenv:** Gestión de variables de entorno para seguridad.
* **DBeaver:** Cliente SQL para análisis exploratorio.

---

## Características Nivel Producción (Enterprise-Grade)

A diferencia de un script básico, este pipeline incorpora buenas prácticas de la industria:

1.  **Seguridad (Gestión de Credenciales):** Las contraseñas y datos de conexión están aislados mediante variables de entorno (`.env`), evitando la exposición de datos sensibles en el código fuente.
2.  **Idempotencia (UPSERT):** El proceso de carga utiliza `ON CONFLICT DO UPDATE`. El pipeline puede ejecutarse 1 o 100 veces sin generar registros duplicados, asegurando la integridad de los datos.
3.  **Tolerancia a Fallos:** Implementación de bloques `try-except-finally` con `rollback` automático en PostgreSQL para evitar transacciones corruptas si el flujo se interrumpe.
4.  **Modelado Dimensional:** Los datos crudos se transforman en un **Modelo Estrella (Star Schema)** para optimizar las consultas analíticas.

---

## Data Warehouse: Modelo Estrella

Para facilitar el análisis a los equipos de BI, los datos transaccionales se modelaron separando las métricas de sus contextos:

```text
                 dim_cliente
                      |
                      |
dim_producto ---- fact_ventas ---- dim_region
                      |
                      |
                  dim_fecha

---

## Business Insights (Análisis SQL)

El modelo construido permite responder rápidamente a preguntas críticas de negocio.

Ejemplo: Penetración de Mercado Regional
Identifica qué regiones generan el mayor volumen de ingresos para priorizar esfuerzos logísticos y de marketing.

SELECT
    r.region_nombre,
    SUM(f.precio) AS total_ventas
FROM fact_ventas f
JOIN dim_region r ON f.region_id = r.region_id
GROUP BY r.region_nombre
ORDER BY total_ventas DESC;

---

## Cómo ejecutar este proyecto localmente
Si deseas clonar y probar este pipeline en tu máquina, sigue estos pasos:

1. Clonar el repositorio

Bash
git clone [https://github.com/tu_usuario/data-engineering-learning.git](https://github.com/tu_usuario/data-engineering-learning.git)
cd data-engineering-learning

2. Instalar dependencias

Bash
pip install pandas psycopg2 python-dotenv

3. Configurar variables de entorno (Seguridad)
Crea un archivo llamado .env en la raíz del proyecto y añade tus credenciales locales de PostgreSQL:

Fragmento de código
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña

4. Ejecutar el Pipeline ETL
Para ejecutar el proceso completo, tienes dos opciones:
* **Automatizado (Windows):** Haz doble clic en el archivo `run_pipeline.bat`.
* **Manual (Terminal):** Ejecuta `python python/cargar_ventas_postgres.py`.

---