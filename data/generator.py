"""Generador de datos de ventas de ejemplo."""

import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from utils.config import CATEGORIAS


@st.cache_data
def generar_datos(dias: int = 90) -> pd.DataFrame:
    """Genera un DataFrame con datos de ventas sintéticos.

    Args:
        dias: Número de días históricos a generar.

    Returns:
        DataFrame con columnas Fecha, Categoría, Ventas, Unidades, Clientes.
    """
    dates = [datetime.now() - timedelta(days=i) for i in range(dias)]
    data = []
    for date in dates:
        for cat in CATEGORIAS:
            data.append({
                "Fecha": date,
                "Categoría": cat,
                "Ventas": random.randint(500, 5000),
                "Unidades": random.randint(10, 200),
                "Clientes": random.randint(5, 100)
            })
    return pd.DataFrame(data)
