"""Funciones de apoyo para fechas (hora de Colombia) y valores decimales."""
# date: solo fecha; datetime: fecha y hora; time: solo hora; timedelta: diferencia de tiempo; timezone: zona horaria
from datetime import date, datetime, time, timedelta, timezone
# Decimal: números exactos para dinero; ROUND_HALF_UP: redondeo normal (0.5 sube)
from decimal import ROUND_HALF_UP, Decimal

# Colombia no tiene horario de verano: America/Bogota siempre es UTC-5
JB_ZONA_BOGOTA = timezone(timedelta(hours=-5), "America/Bogota")
# Molde para redondear a 2 decimales (dinero), como DECIMAL(10,2)
JB_DOS_DECIMALES = Decimal("0.01")
# Molde para redondear a 3 decimales (cantidades de insumos), como DECIMAL(10,3)
JB_TRES_DECIMALES = Decimal("0.001")


# Función que devuelve la fecha y hora actual de Colombia
def jb_ahora() -> datetime:
    """Fecha y hora actual de Colombia, sin zona horaria (así se guarda en los DATETIME de MySQL)."""
    # Toma la hora actual en Bogotá, le quita la zona horaria y los microsegundos
    return datetime.now(JB_ZONA_BOGOTA).replace(tzinfo=None, microsecond=0)


# Función que devuelve la fecha de hoy en Colombia
def jb_hoy() -> date:
    # Toma solo la fecha de la hora actual de Bogotá
    return datetime.now(JB_ZONA_BOGOTA).date()


# Función que pasa a hora de Colombia una fecha que llega en otra zona horaria
def jb_hora_colombia(jb_fecha: datetime) -> datetime:
    """Si la fecha trae zona horaria (por ejemplo, terminada en Z), la pasa a hora de Colombia sin zona."""
    # tzinfo distinto de None significa que la fecha trae zona horaria
    if jb_fecha.tzinfo is not None:
        # La convierte a hora de Bogotá y le quita la zona horaria
        jb_fecha = jb_fecha.astimezone(JB_ZONA_BOGOTA).replace(tzinfo=None)
    # Devuelve la fecha sin microsegundos
    return jb_fecha.replace(microsecond=0)


# Función que convierte una fecha en el primer instante de ese día
def jb_inicio_del_dia(jb_fecha: date) -> datetime:
    # time.min es 00:00:00: une la fecha con esa hora
    return datetime.combine(jb_fecha, time.min)


# Función que redondea dinero
def jb_dinero(jb_valor) -> Decimal:
    """Redondea un valor de dinero a 2 decimales, como DECIMAL(10,2)."""
    # Convierte el valor en Decimal y lo redondea a 0.01
    return Decimal(jb_valor).quantize(JB_DOS_DECIMALES, rounding=ROUND_HALF_UP)


# Función que redondea cantidades de insumos
def jb_cantidad(jb_valor) -> Decimal:
    """Redondea una cantidad de insumo a 3 decimales, como DECIMAL(10,3)."""
    # Convierte el valor en Decimal y lo redondea a 0.001
    return Decimal(jb_valor).quantize(JB_TRES_DECIMALES, rounding=ROUND_HALF_UP)
