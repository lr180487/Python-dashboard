"""Plotly visualization components."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_pie_chart(df: pd.DataFrame) -> None:
    """Render pie chart: sales by category."""
    ventas_por_categoria = df.groupby("Categoría")["Ventas"].sum().reset_index()
    fig = px.pie(
        ventas_por_categoria,
        values="Ventas",
        names="Categoría",
        title="Sales by Category",
        hole=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_line_chart(df: pd.DataFrame) -> None:
    """Render line chart: daily sales trend."""
    ventas_diarias = df.groupby("Fecha")["Ventas"].sum().reset_index().sort_values("Fecha")
    fig = px.line(
        ventas_diarias,
        x="Fecha",
        y="Ventas",
        title="Daily Sales Trend",
        markers=True,
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Sales ($)")
    st.plotly_chart(fig, use_container_width=True)


def render_charts(df: pd.DataFrame) -> None:
    """Render both charts side by side."""
    st.subheader("Visualizations")
    col_left, col_right = st.columns(2)

    with col_left:
        render_pie_chart(df)
    with col_right:
        render_line_chart(df)
