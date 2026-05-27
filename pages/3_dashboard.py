"""Dashboard completo con métricas, gráficos y filtros."""

from datetime import datetime

import streamlit as st
from auth.auth_manager import get_authenticator
from components.charts import render_charts
from components.metrics import render_metrics
from data.generator import generar_datos
from utils.config import CATEGORIAS, PERIODOS, DashboardConfig
from utils.filters import filtrar_por_categoria, filtrar_por_periodo

# ── Guardia de seguridad ──
if not st.session_state.get("authentication_status"):
    st.warning("Debes iniciar sesión para acceder al dashboard.")
    if st.button("Ir al Login"):
        st.switch_page("pages/2_login.py")
    st.stop()

# ── Autenticador para logout ──
authenticator, _ = get_authenticator()

# ── Sidebar: usuario + logout + filtros ──
st.sidebar.title("Panel de Control")
name = st.session_state.get("name", "Usuario")
st.sidebar.write(f"Bienvenido, **{name}** 👋")
authenticator.logout("Cerrar Sesión", "sidebar")
st.sidebar.divider()

st.sidebar.header("Filtros")
periodo = st.sidebar.selectbox("Período", PERIODOS)
categoria = st.sidebar.multiselect("Categoría", CATEGORIAS, default=CATEGORIAS)

# ── Main content ──
cfg = DashboardConfig()
st.title(f"{cfg.icon} {cfg.title}")
st.markdown(cfg.subtitle)

# Datos
_df = generar_datos(cfg.dias_historicos)
df_filtrado = filtrar_por_periodo(_df, periodo)
df_filtrado = filtrar_por_categoria(df_filtrado, categoria)

# Métricas
render_metrics(df_filtrado)

# Gráficos
render_charts(df_filtrado)

# Tabla detallada
st.subheader("Datos Detallados")
st.dataframe(df_filtrado.sort_values("Fecha", ascending=False), width="stretch")

# Footer
st.markdown("---")
st.caption(f"Dashboard actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
