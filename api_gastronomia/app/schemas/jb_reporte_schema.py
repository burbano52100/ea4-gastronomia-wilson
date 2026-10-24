"""Esquemas de los reportes de ventas (RF11)."""
# date: solo fecha (sin hora)
from datetime import date

# BaseModel: clase base de Pydantic
from pydantic import BaseModel

# JbNumero: decimal que se responde como número
from app.schemas.jb_tipos import JbNumero


# Respuesta de GET /reportes/ventas
class JbReporteVentas(BaseModel):
    # Fecha inicial del rango
    desde: date
    # Fecha final del rango
    hasta: date
    # Cuántos pedidos ENTREGADOS hay en el rango
    numero_pedidos: int
    # Suma de los totales de esos pedidos
    total_vendido: JbNumero
    # total_vendido / numero_pedidos
    ticket_promedio: JbNumero


# Un producto del ranking de GET /reportes/productos-mas-vendidos
class JbProductoVendido(BaseModel):
    # Puesto en el ranking (1 = el más vendido)
    posicion: int
    # Id del producto
    id_producto: int
    # Nombre del producto; null si el producto ya no existe
    nombre: str | None = None
    # Unidades vendidas
    cantidad_vendida: int
    # En cuántos pedidos aparece
    numero_pedidos: int
    # Dinero que generó
    total_vendido: JbNumero
