from datetime import datetime
from dominio.excepciones import DatoInvalidoError, EstadoCitaInvalidoError

ESTADOS_CITA_VALIDOS = ("Pendiente", "Confirmada", "Completada", "Cancelada")


def validar_texto_no_vacio(valor: str, campo: str, min_len: int = 2, max_len: int = 120) -> str:
    if not isinstance(valor, str):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser texto.")
    limpio = " ".join(valor.strip().split())
    if len(limpio) < min_len:
        raise DatoInvalidoError(f"El campo '{campo}' debe tener al menos {min_len} caracteres.")
    if len(limpio) > max_len:
        raise DatoInvalidoError(f"El campo '{campo}' no puede superar {max_len} caracteres.")
    return limpio


def validar_telefono(telefono: str) -> str:
    if not isinstance(telefono, str):
        raise DatoInvalidoError("El teléfono debe ser texto.")
    limpio = telefono.strip()
    # Permite dígitos, espacios, guiones y '+' inicial; exige al menos 7 dígitos reales
    solo_digitos = "".join(ch for ch in limpio if ch.isdigit())
    permitidos = set("0123456789+-() ")
    if not limpio or not set(limpio).issubset(permitidos) or len(solo_digitos) < 7:
        raise DatoInvalidoError("Ingresa un número de teléfono válido (al menos 7 dígitos).")
    return limpio


def validar_numero_positivo(valor, campo: str, es_entero: bool = False):
    if isinstance(valor, bool):
        raise DatoInvalidoError(f"El campo '{campo}' no es un número válido.")
    try:
        numero = int(valor) if es_entero else float(valor)
    except (TypeError, ValueError) as exc:
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número válido.") from exc

    if numero <= 0:
        raise DatoInvalidoError(f"El campo '{campo}' debe ser mayor que cero.")
    return numero


def validar_fecha_hora(fecha_hora) -> datetime:
    if isinstance(fecha_hora, datetime):
        return fecha_hora
    if isinstance(fecha_hora, str):
        texto = fecha_hora.strip()
        for formato in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(texto, formato)
            except ValueError:
                continue
    raise DatoInvalidoError("La fecha y hora no tienen un formato válido (usa AAAA-MM-DD HH:MM).")


def validar_estado_cita(estado: str) -> str:
    if not isinstance(estado, str) or estado not in ESTADOS_CITA_VALIDOS:
        estados_str = ", ".join(ESTADOS_CITA_VALIDOS)
        raise EstadoCitaInvalidoError(f"Estado '{estado}' inválido. Usa uno de: {estados_str}.")
    return estado