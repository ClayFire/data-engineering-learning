-- Crear tabla de ventas
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    cliente TEXT,
    producto TEXT,
    precio INT,
    fecha DATE,
    region TEXT
);

-- Insertar datos de ejemplo
INSERT INTO ventas (cliente, producto, precio, fecha, region) VALUES
('Ana', 'Laptop', 900000, '2024-01-10', 'Santiago'),
('Pedro', 'Mouse', 20000, '2024-01-12', 'Valparaiso'),
('Ana', 'Teclado', 50000, '2024-01-15', 'Santiago'),
('Maria', 'Laptop', 850000, '2024-01-20', 'Concepcion'),
('Pedro', 'Monitor', 200000, '2024-01-22', 'Valparaiso');

-- Ver todas las ventas
SELECT * FROM ventas;

-- Ventas totales por cliente
SELECT cliente, SUM(precio)
FROM ventas
GROUP BY cliente;

-- Cantidad de ventas por región
SELECT region, COUNT(*)
FROM ventas
GROUP BY region;

-- Cantidad de ventas por región de mayor a menor monto
SELECT region, SUM(precio) AS total_ventas
FROM ventas_pipeline
GROUP BY region
ORDER BY total_ventas DESC;

-- Venta más cara
SELECT *
FROM ventas
ORDER BY precio DESC
LIMIT 1;

-- Anula registros duplicados al querer insertar uno que ya existe
ALTER TABLE ventas_pipeline
ADD CONSTRAINT unique_venta
UNIQUE (cliente, producto, fecha);
