"""Componente de métricas principales."""

import pandas as pd
import streamlit as st


def render_metrics(df: pd.DataFrame):
    """Renderiza las 4 métricas principales en columnas.

    Args:
        df: DataFrame filtrado con columnas Ventas, Unidades, Clientes.
    """
    st.subheader("Métricas Principales")
    col1, col2, col3, col4 = st.columns(4)

    total_ventas = df["Ventas"].sum()
    total_unidades = df["Unidades"].sum()
    total_clientes = df["Clientes"].sum()
    promedio_venta = total_ventas / total_unidades if total_unidades > 0 else 0

    with col1:
        st.metric("Ventas Totales", f"${total_ventas:,}")
    with col2:
        st.metric("Unidades Vendidas", f"{total_unidades:,}")
    with col3:
        st.metric("Clientes", f"{total_clientes:,}")
    with col4:
        st.metric("Venta Promedio", f"${promedio_venta:.2f}")
