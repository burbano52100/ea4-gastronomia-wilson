"""Acceso a la colección insumos (inventario)."""
# datetime: fecha y hora
from datetime import datetime
# Decimal: números exactos para cantidades y costos
from decimal import Decimal

# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de insumos: hereda el CRUD y agrega consultas y movimientos de inventario
class JbInsumoRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "insumos"; el _id se responde como "id_insumo"
        super().__init__("insumos", "id_insumo")

    # Reemplaza el formateo del repositorio base para ajustar la fecha de vencimiento
    def jb_formatear(self, jb_documento: dict | None) -> dict | None:
        # MongoDB guarda fechas con hora; el vencimiento se responde solo como fecha.
        jb_documento = super().jb_formatear(jb_documento)
        # Si hay documento y la fecha de vencimiento viene como fecha con hora...
        if jb_documento is not None and isinstance(jb_documento.get("fecha_vencimiento"), datetime):
            # ...se deja solo la fecha
            jb_documento["fecha_vencimiento"] = jb_documento["fecha_vencimiento"].date()
        # Devuelve el documento formateado
        return jb_documento

    # Insumos activos con stock en el mínimo o por debajo (RF07)
    def jb_stock_bajo(self) -> list[dict]:
        # $expr permite comparar dos campos del mismo documento: stock_actual <= stock_minimo
        return self.jb_listar({"estado": "ACTIVO", "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}})

    # Insumos activos que vencen entre dos fechas (RF07)
    def jb_por_vencer(self, jb_desde: datetime, jb_hasta: datetime) -> list[dict]:
        # Lista con filtro y orden
        return self.jb_listar(
            # Activos con fecha de vencimiento entre desde ($gte = mayor o igual) y hasta ($lte = menor o igual)
            {"estado": "ACTIVO", "fecha_vencimiento": {"$gte": jb_desde, "$lte": jb_hasta}},
            # Primero los que vencen antes
            [("fecha_vencimiento", 1)],
        )

    # Suma o resta existencias
    def jb_cambiar_stock(self, jb_id: int, jb_cantidad: Decimal) -> None:
        """Suma (cantidad positiva) o resta (cantidad negativa) existencias."""
        # $inc suma la cantidad al valor actual en una sola operación
        self.jb_coleccion.update_one({"_id": jb_id}, {"$inc": {"stock_actual": jb_cantidad}})

    # Entrada de inventario por una compra
    def jb_registrar_entrada(self, jb_id: int, jb_cantidad: Decimal, jb_costo_unitario: Decimal) -> None:
        """RN02: una compra suma existencias y actualiza el costo unitario."""
        # Una sola actualización con dos cambios
        self.jb_coleccion.update_one(
            # El insumo comprado
            {"_id": jb_id},
            # $inc suma la cantidad comprada al stock; $set pone el costo unitario de la compra
            {"$inc": {"stock_actual": jb_cantidad}, "$set": {"costo_unitario": jb_costo_unitario}},
        )

    # Cambia solo el costo unitario
    def jb_actualizar_costo(self, jb_id: int, jb_costo_unitario: Decimal) -> None:
        # $set reemplaza el costo unitario
        self.jb_coleccion.update_one({"_id": jb_id}, {"$set": {"costo_unitario": jb_costo_unitario}})

    # Descuenta inventario solo si alcanza (RN03)
    def jb_descontar_si_alcanza(self, jb_id: int, jb_cantidad: Decimal) -> bool:
        """Descuenta solo si hay existencias suficientes. Devuelve False si no alcanzó."""
        # Actualización condicional: MongoDB revisa la condición y resta en un solo paso
        jb_resultado = self.jb_coleccion.update_one(
            # Condición: el insumo y que tenga stock mayor o igual a lo que se va a restar
            {"_id": jb_id, "stock_actual": {"$gte": jb_cantidad}},
            # $inc con número negativo resta
            {"$inc": {"stock_actual": -jb_cantidad}},
        )
        # Si se modificó un documento, sí alcanzó; si no, no había stock suficiente
        return jb_resultado.modified_count == 1


# Instancia única que usan los servicios
jb_insumo_repository = JbInsumoRepository()
