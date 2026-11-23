from datetime import datetime
from dominio.validaciones import (
    ESTADOS_CITA_VALIDOS,
    validar_estado_cita,
    validar_fecha_hora,
    validar_numero_positivo,
    validar_telefono,
    validar_texto_no_vacio,
)


class Persona:
    """Clase base que encapsula datos básicos de una persona."""

    def __init__(self, nombre: str, telefono: str):
        self.nombre = nombre
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = validar_texto_no_vacio(valor, "nombre", min_len=2, max_len=100)

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = validar_telefono(valor)

    def __str__(self) -> str:
        return f"{self._nombre} ({self._telefono})"


class Cliente(Persona):
    """Subclase de Persona que representa a un cliente del salón."""

    def __init__(self, nombre: str, telefono: str, notas: str = "", cliente_id: int | None = None):
        super().__init__(nombre=nombre, telefono=telefono)
        self.cliente_id = cliente_id
        self.notas = notas

    @property
    def notas(self) -> str:
        return self._notas

    @notas.setter
    def notas(self, valor: str) -> None:
        if valor is None:
            self._notas = ""
            return
        if not isinstance(valor, str):
            self._notas = str(valor).strip()
            return
        self._notas = valor.strip()[:250]

    def __repr__(self) -> str:
        return f"Cliente(id={self.cliente_id}, nombre={self.nombre!r}, telefono={self.telefono!r})"


class Servicio:
    """Representa un servicio ofrecido (ej. Corte, Barba, Alisado)."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        duracion_min: int,
        servicio_id: int | None = None,
    ):
        self.servicio_id = servicio_id
        self.nombre = nombre
        self.precio = precio
        self.duracion_min = duracion_min

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = validar_texto_no_vacio(valor, "servicio", min_len=2, max_len=80)

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        self._precio = float(validar_numero_positivo(valor, "precio", es_entero=False))

    @property
    def duracion_min(self) -> int:
        return self._duracion_min

    @duracion_min.setter
    def duracion_min(self, valor: int) -> None:
        self._duracion_min = int(validar_numero_positivo(valor, "duración (min)", es_entero=True))

    def __str__(self) -> str:
        return f"{self._nombre} (${self._precio:.2f} · {self._duracion_min} min)"


class Cita:
    """Representa una cita programada vinculando un Cliente y un Servicio."""

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        fecha_hora: datetime | str,
        estado: str = "Pendiente",
        cita_id: int | None = None,
    ):
        self.cita_id = cita_id
        self.cliente = cliente
        self.servicio = servicio
        self.fecha_hora = fecha_hora
        self.estado = estado

    @property
    def fecha_hora(self) -> datetime:
        return self._fecha_hora

    @fecha_hora.setter
    def fecha_hora(self, valor: datetime | str) -> None:
        self._fecha_hora = validar_fecha_hora(valor)

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        self._estado = validar_estado_cita(valor)

    def cambiar_estado(self, nuevo_estado: str) -> None:
        self.estado = nuevo_estado

    def confirmar(self) -> None:
        self.cambiar_estado("Confirmada")

    def completar(self) -> None:
        self.cambiar_estado("Completada")

    def cancelar(self) -> None:
        self.cambiar_estado("Cancelada")

    def fecha_hora_formateada(self) -> str:
        return self._fecha_hora.strftime("%Y-%m-%d %H:%M")

    def resumen(self) -> str:
        return (
            f"[{self._estado}] {self.fecha_hora_formateada()} - "
            f"{self.cliente.nombre} -> {self.servicio.nombre}"
        )