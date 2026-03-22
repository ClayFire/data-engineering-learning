@echo off
title ETL Ventas Pipeline
color 0A

echo ===================================================
echo      INICIANDO PIPELINE DE DATOS (ETL)
echo ===================================================
echo.

:: Magia de Windows: Obligamos a la terminal a ubicarse en la carpeta exacta de este archivo
cd /d "%~dp0"

:: Ejecutamos el script de Python (usando la misma ruta relativa que ya probamos)
python python\cargar_ventas_postgres.py

echo.
echo ===================================================
echo      PROCESO FINALIZADO
echo ===================================================
pause