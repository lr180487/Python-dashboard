"""Sales Dashboard with Streamlit."""

import random
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # noqa: F401
import streamlit as st

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    page_icon="📊",
)

st.title("📊 Sales Dashboard")
st.markdown("Interactive control panel with key metrics and visualizations.")


@st.cache_data
def generar_datos(dias: int = 90) -> pd.DataFrame:
    """Generate sample sales data."""
    dates = [datetime.now() - timedelta(days=i) for i in range(dias)]
    categorias = ["Electronics", "Clothing", "Home", "Sports"]
    data = []

    for date in dates:
        for categoria in categorias:
            data.append(
                {
                    "Fecha": date,
                    "Categoría": categoria,
                    "Ventas": random.randint(500, 5000),
                    "Unidades": random.randint(10, 200),
                    "Clientes": random.randint(5, 100),
                }
            )

    return pd.DataFrame(data)


st.sidebar.header("Filters")
periodo = st.sidebar.selectbox(
    "Period",
    ["Last 7 days", "Last 30 days", "Last 90 days"],
)
categoria = st.sidebar.multiselect(
    "Category",
    ["Electronics", "Clothing", "Home", "Sports"],
    default=["Electronics", "Clothing", "Home", "Sports"],
)

df = generar_datos()

period_map = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
}

days = period_map.get(periodo, 90)
df_filtrado = df[df["Fecha"] >= datetime.now() - timedelta(days=days)]
df_filtrado = df_filtrado[df_filtrado["Categoría"].isin(categoria)]

st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_ventas = df_filtrado["Ventas"].sum()
total_unidades = df_filtrado["Unidades"].sum()
total_clientes = df_filtrado["Clientes"].sum()
promedio_venta = total_ventas / total_unidades if total_unidades > 0 else 0

with col1:
    st.metric("Total Sales", f"${total_ventas:,}")
with col2:
    st.metric("Units Sold", f"{total_unidades:,}")
with col3:
    st.metric("Customers", f"{total_clientes:,}")
with col4:
    st.metric("Average Sale", f"${promedio_venta:.2f}")

st.subheader("Visualizations")
col_left, col_right = st.columns(2)

with col_left:
    ventas_por_categoria = df_filtrado.groupby("Categoría")["Ventas"].sum().reset_index()
    fig_pie = px.pie(
        ventas_por_categoria,
        values="Ventas",
        names="Categoría",
        title="Sales by Category",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    ventas_diarias = df_filtrado.groupby("Fecha")["Ventas"].sum().reset_index()
    fig_line = px.line(
        ventas_diarias,
        x="Fecha",
        y="Ventas",
        title="Daily Sales Trend",
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Detailed Data")
st.dataframe(
    df_filtrado.sort_values("Fecha", ascending=False),
    use_container_width=True,
)

st.markdown("---")
st.caption(f"Dashboard updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
