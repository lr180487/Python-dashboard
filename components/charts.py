"""Componentes de visualización con Plotly."""

import plotly.express as px
import streamlit as st
import pandas as pd


def render_pie_chart(df: pd.DataFrame):
    """Gráfico de pastel: ventas por categoría."""
    ventas_por_categoria = df.groupby("Categoría")["Ventas"].sum().reset_index()
    fig = px.pie(
        ventas_por_categoria,
        values="Ventas",
        names="Categoría",
        title="Ventas por Categoría",
        hole=0.3
    )
    st.plotly_chart(fig, width="stretch")


def render_line_chart(df: pd.DataFrame):
    """Gráfico de línea: tendencia de ventas diarias."""
    ventas_diarias = df.groupby("Fecha")["Ventas"].sum().reset_index().sort_values("Fecha")
    fig = px.line(
        ventas_diarias,
        x="Fecha",
        y="Ventas",
        title="Tendencia de Ventas Diarias",
        markers=True
    )
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Ventas ($)")
    st.plotly_chart(fig, width="stretch")


def render_charts(df: pd.DataFrame):
    """Renderiza ambos gráficos lado a lado."""
    st.subheader("Visualizaciones")
    col_left, col_right = st.columns(2)
    with col_left:
        render_pie_chart(df)
    with col_right:
        render_line_chart(df)
