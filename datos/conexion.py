import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_BD = BASE_DIR / "db.sqlite3"

SERVICIOS_INICIALES = [
    ("Corte clásico", 8.00, 30),
    ("Barba y perfilado", 6.00, 20),
    ("Corte y peinado", 12.00, 45),
    ("Alisado o tratamiento", 25.00, 60),
]


def obtener_conexion() -> sqlite3.Connection:
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


def inicializar_bd() -> None:
    with obtener_conexion() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                notas TEXT NOT NULL DEFAULT ''
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                precio REAL NOT NULL CHECK(precio > 0),
                duracion_min INTEGER NOT NULL CHECK(duracion_min > 0)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                servicio_id INTEGER NOT NULL,
                fecha_hora TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE,
                FOREIGN KEY (servicio_id) REFERENCES servicios (id) ON DELETE RESTRICT
            );
            """
        )

        cursor.execute("SELECT COUNT(*) AS total FROM servicios;")
        total_servicios = cursor.fetchone()["total"]
        if total_servicios == 0:
            cursor.executemany(
                """
                INSERT INTO servicios (nombre, precio, duracion_min)
                VALUES (?, ?, ?);
                """,
                SERVICIOS_INICIALES,
            )

        conn.commit()