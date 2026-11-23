class ErrorDominio(Exception):
    """Excepción base para errores de lógica y reglas de negocio."""


class DatoInvalidoError(ErrorDominio):
    """Se lanza cuando un campo o valor no cumple las reglas de validación."""


class EstadoCitaInvalidoError(ErrorDominio):
    """Se lanza cuando se intenta asignar o transicionar a un estado no válido."""