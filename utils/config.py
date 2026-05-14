"""Configuración global del dashboard."""

from dataclasses import dataclass
from typing import List


@dataclass
class DashboardConfig:
    title: str = "Dashboard de Ventas"
    subtitle: str = "Panel de control interactivo con métricas clave y visualizaciones."
    icon: str = "📊"
    layout: str = "wide"
    dias_historicos: int = 90


CATEGORIAS: List[str] = ["Electrónica", "Ropa", "Hogar", "Deportes"]
PERIODOS: List[str] = ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días"]
