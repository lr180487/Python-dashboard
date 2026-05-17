import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Dashboard de Ventas", layout="wide", page_icon="📊")

st.title("📊 Dashboard de Ventas")
st.markdown("Panel de control interactivo con métricas clave y visualizaciones.")

# Sidebar
st.sidebar.header("Filtros")
periodo = st.sidebar.selectbox(
    "Período",
    ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días"],
)
categoria = st.sidebar.multiselect(
    "Categoría",
    ["Electrónica", "Ropa", "Hogar", "Deportes"],
    default=["Electrónica", "Ropa", "Hogar", "Deportes"],
)


# Generar datos de ejemplo
@st.cache_data
def generar_datos():
    dates = [datetime.now() - timedelta(days=i) for i in range(90)]
    categorias = ["Electrónica", "Ropa", "Hogar", "Deportes"]
    data = []
    for date in dates:
        for cat in categorias:
            data.append(
                {
                    "Fecha": date,
                    "Categoría": cat,
                    "Ventas": random.randint(500, 5000),
                    "Unidades": random.randint(10, 200),
                    "Clientes": random.randint(5, 100),
                }
            )
    return pd.DataFrame(data)


df = generar_datos()

# Filtrar por período
if periodo == "Últimos 7 días":
    df_filtrado = df[df["Fecha"] >= datetime.now() - timedelta(days=7)]
elif periodo == "Últimos 30 días":
    df_filtrado = df[df["Fecha"] >= datetime.now() - timedelta(days=30)]
else:
    df_filtrado = df[df["Fecha"] >= datetime.now() - timedelta(days=90)]

df_filtrado = df_filtrado[df_filtrado["Categoría"].isin(categoria)]

# Métricas
st.subheader("Métricas Principales")
col1, col2, col3, col4 = st.columns(4)
total_ventas = df_filtrado["Ventas"].sum()
total_unidades = df_filtrado["Unidades"].sum()
total_clientes = df_filtrado["Clientes"].sum()
promedio_venta = total_ventas / total_unidades if total_unidades > 0 else 0

with col1:
    st.metric("Ventas Totales", f"${total_ventas:,}")
with col2:
    st.metric("Unidades Vendidas", f"{total_unidades:,}")
with col3:
    st.metric("Clientes", f"{total_clientes:,}")
with col4:
    st.metric("Venta Promedio", f"${promedio_venta:.2f}")

# Gráficos
st.subheader("Visualizaciones")
col_left, col_right = st.columns(2)

with col_left:
    ventas_por_categoria = df_filtrado.groupby("Categoría")["Ventas"].sum().reset_index()
    fig_pie = px.pie(
        ventas_por_categoria,
        values="Ventas",
        names="Categoría",
        title="Ventas por Categoría",
    )
    st.plotly_chart(fig_pie, width="stretch")

with col_right:
    ventas_diarias = df_filtrado.groupby("Fecha")["Ventas"].sum().reset_index()
    fig_line = px.line(
        ventas_diarias, x="Fecha", y="Ventas", title="Tendencia de Ventas Diarias"
    )
    st.plotly_chart(fig_line, width="stretch")

# Tabla de datos
st.subheader("Datos Detallados")
st.dataframe(df_filtrado.sort_values("Fecha", ascending=False), width="stretch")

# Barra de estado
st.markdown("---")
st.caption(
    f"Dashboard actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)
