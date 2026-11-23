from datetime import datetime
from datos.conexion import inicializar_bd, obtener_conexion
from dominio.excepciones import DatoInvalidoError
from dominio.modelos_poo import Cita, Cliente, Servicio
from dominio.validaciones import (
    validar_estado_cita,
    validar_fecha_hora,
    validar_numero_positivo,
    validar_telefono,
    validar_texto_no_vacio,
)


def crear_o_obtener_cliente(nombre: str, telefono: str, notas: str = "") -> Cliente:
    inicializar_bd()
    cliente_obj = Cliente(nombre=nombre, telefono=telefono, notas=notas)

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, telefono, notas
            FROM clientes
            WHERE telefono = ? AND LOWER(nombre) = LOWER(?);
            """,
            (cliente_obj.telefono, cliente_obj.nombre),
        )
        fila = cursor.fetchone()
        if fila:
            cliente_obj.cliente_id = fila["id"]
            if cliente_obj.notas and cliente_obj.notas != fila["notas"]:
                cursor.execute(
                    "UPDATE clientes SET notas = ? WHERE id = ?;",
                    (cliente_obj.notas, fila["id"]),
                )
                conn.commit()
            return cliente_obj

        cursor.execute(
            """
            INSERT INTO clientes (nombre, telefono, notas)
            VALUES (?, ?, ?);
            """,
            (cliente_obj.nombre, cliente_obj.telefono, cliente_obj.notas),
        )
        conn.commit()
        cliente_obj.cliente_id = cursor.lastrowid
        return cliente_obj


def crear_servicio(nombre: str, precio: float, duracion_min: int) -> Servicio:
    inicializar_bd()
    servicio_obj = Servicio(nombre=nombre, precio=precio, duracion_min=duracion_min)

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO servicios (nombre, precio, duracion_min)
            VALUES (?, ?, ?);
            """,
            (servicio_obj.nombre, servicio_obj.precio, servicio_obj.duracion_min),
        )
        conn.commit()
        servicio_obj.servicio_id = cursor.lastrowid
        return servicio_obj


def listar_servicios() -> list[dict]:
    inicializar_bd()
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, precio, duracion_min
            FROM servicios
            ORDER BY nombre ASC;
            """
        )
        return [dict(fila) for fila in cursor.fetchall()]


def obtener_servicio_por_id(servicio_id: int) -> Servicio | None:
    inicializar_bd()
    sid = int(validar_numero_positivo(servicio_id, "servicio_id", es_entero=True))
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nombre, precio, duracion_min
            FROM servicios
            WHERE id = ?;
            """,
            (sid,),
        )
        fila = cursor.fetchone()
        if not fila:
            return None
        return Servicio(
            nombre=fila["nombre"],
            precio=fila["precio"],
            duracion_min=fila["duracion_min"],
            servicio_id=fila["id"],
        )


def crear_cita(
    nombre_cliente: str,
    telefono_cliente: str,
    servicio_id: int,
    fecha_hora: datetime | str,
    notas_cliente: str = "",
) -> Cita:
    inicializar_bd()
    servicio = obtener_servicio_por_id(servicio_id)
    if servicio is None:
        raise DatoInvalidoError("El servicio seleccionado no existe.")

    cliente = crear_o_obtener_cliente(
        nombre=nombre_cliente,
        telefono=telefono_cliente,
        notas=notas_cliente,
    )
    cita_obj = Cita(
        cliente=cliente,
        servicio=servicio,
        fecha_hora=fecha_hora,
        estado="Pendiente",
    )

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO citas (cliente_id, servicio_id, fecha_hora, estado)
            VALUES (?, ?, ?, ?);
            """,
            (
                cliente.cliente_id,
                servicio.servicio_id,
                cita_obj.fecha_hora_formateada(),
                cita_obj.estado,
            ),
        )
        conn.commit()
        cita_obj.cita_id = cursor.lastrowid
        return cita_obj


def listar_citas(estado: str | None = None, fecha: str | None = None) -> list[dict]:
    inicializar_bd()
    consultas = [
        """
        SELECT
            c.id,
            c.fecha_hora,
            c.estado,
            cl.id AS cliente_id,
            cl.nombre AS cliente_nombre,
            cl.telefono AS cliente_telefono,
            cl.notas AS cliente_notas,
            s.id AS servicio_id,
            s.nombre AS servicio_nombre,
            s.precio AS servicio_precio,
            s.duracion_min AS servicio_duracion
        FROM citas c
        INNER JOIN clientes cl ON c.cliente_id = cl.id
        INNER JOIN servicios s ON c.servicio_id = s.id
        WHERE 1 = 1
        """
    ]
    parametros: list = []

    if estado and estado != "Todas":
        estado_limpio = validar_estado_cita(estado)
        consultas.append("AND c.estado = ?")
        parametros.append(estado_limpio)

    if fecha:
        fecha_limpia = validar_texto_no_vacio(fecha, "fecha", min_len=8, max_len=15)
        consultas.append("AND c.fecha_hora LIKE ?")
        parametros.append(f"{fecha_limpia}%")

    consultas.append("ORDER BY c.fecha_hora ASC, c.id DESC;")
    sql = "\n".join(consultas)

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, parametros)
        return [dict(fila) for fila in cursor.fetchall()]


def actualizar_estado_cita(cita_id: int, nuevo_estado: str) -> bool:
    inicializar_bd()
    cid = int(validar_numero_positivo(cita_id, "cita_id", es_entero=True))
    estado_valido = validar_estado_cita(nuevo_estado)

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE citas SET estado = ? WHERE id = ?;",
            (estado_valido, cid),
        )
        conn.commit()
        return cursor.rowcount > 0


def reprogramar_cita(cita_id: int, nueva_fecha_hora: datetime | str) -> bool:
    inicializar_bd()
    cid = int(validar_numero_positivo(cita_id, "cita_id", es_entero=True))
    dt = validar_fecha_hora(nueva_fecha_hora)
    texto_fh = dt.strftime("%Y-%m-%d %H:%M")

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE citas SET fecha_hora = ? WHERE id = ?;",
            (texto_fh, cid),
        )
        conn.commit()
        return cursor.rowcount > 0


def eliminar_cita(cita_id: int) -> bool:
    inicializar_bd()
    cid = int(validar_numero_positivo(cita_id, "cita_id", es_entero=True))

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citas WHERE id = ?;", (cid,))
        conn.commit()
        return cursor.rowcount > 0