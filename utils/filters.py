"""Utilidades de filtrado de datos."""

from datetime import datetime, timedelta

import pandas as pd

from utils.config import PERIODOS


def filtrar_por_periodo(df: pd.DataFrame, periodo: str) -> pd.DataFrame:
    """Filtra el DataFrame según el período seleccionado.

    Args:
        df: DataFrame con columna 'Fecha'.
        periodo: Uno de los valores definidos en PERIODOS.

    Returns:
        DataFrame filtrado.
    """
    hoy = datetime.now()
    if periodo == PERIODOS[0]:  # Últimos 7 días
        corte = hoy - timedelta(days=7)
    elif periodo == PERIODOS[1]:  # Últimos 30 días
        corte = hoy - timedelta(days=30)
    else:  # Últimos 90 días
        corte = hoy - timedelta(days=90)
    return df[df["Fecha"] >= corte].copy()


def filtrar_por_categoria(df: pd.DataFrame, categorias: list) -> pd.DataFrame:
    """Filtra el DataFrame por categorías seleccionadas.

    Args:
        df: DataFrame con columna 'Categoría'.
        categorias: Lista de nombres de categorías.

    Returns:
        DataFrame filtrado.
    """
    return df[df["Categoría"].isin(categorias)].copy()
