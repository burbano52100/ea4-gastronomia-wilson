"""Esquemas de los reportes (RF11)."""
# date: solo fecha
from datetime import date

# BaseModel: clase base de los esquemas
from pydantic import BaseModel

# Decimal que se responde como número
from app.schemas.jb_tipos import JbNumero


# Respuesta de GET /reportes/ventas
class JbReporteVentas(BaseModel):
    # Fecha inicial del rango (incluida)
    desde: date
    # Fecha final del rango (incluida completa)
    hasta: date
    # Cantidad de pedidos ENTREGADO en el rango
    numero_pedidos: int
    # Suma de los totales de esos pedidos
    total_vendido: JbNumero
    # total_vendido / numero_pedidos (0 si no hubo pedidos)
    promedio_por_pedido: JbNumero


# Un producto del ranking de GET /reportes/productos-mas-vendidos
class JbProductoVendido(BaseModel):
    # Puesto en el ranking (1 = el más vendido)
    posicion: int
    # Id del producto
    id_producto: int
    # Nombre del producto
    nombre: str
    # Suma de las cantidades vendidas
    cantidad_vendida: JbNumero
    # Suma de los subtotales vendidos
    total_vendido: JbNumero
