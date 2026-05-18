"""Landing page atractiva con CTA hacia login."""

import streamlit as st

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Bienvenido",
    page_icon="🚀",
    layout="centered",
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown(
    """
    <style>
    .hero {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }

    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.2rem;
        color: #666;
    }

    .feature-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .cta-container {
        text-align: center;
        padding: 2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# HERO SECTION
# ======================================================
st.markdown(
    """
    <div class="hero">
        <h1>Gestión Inteligente de Ventas</h1>
        <p>
            Visualiza, analiza y toma decisiones
            con datos en tiempo real.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# CTA SECTION
# ======================================================
st.markdown(
    '<div class="cta-container">',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button(
        "🔐 Iniciar Sesión",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/2_login.py")

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

# ======================================================
# FEATURES SECTION
# ======================================================
st.subheader("¿Qué puedes hacer?")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📊</div>

            <h4>Dashboard Interactivo</h4>

            <p>
                Métricas clave y gráficos dinámicos
                filtrables por período y categoría.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔐</div>

            <h4>Autenticación Segura</h4>

            <p>
                Sistema de usuarios con registro,
                login y recuperación de contraseña.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">⚡</div>

            <h4>Respuesta en Tiempo Real</h4>

            <p>
                Datos generados al vuelo con
                visualizaciones rápidas y responsivas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ======================================================
# FOOTER
# ======================================================
st.divider()

st.caption("© 2026 · Dashboard de Ventas · " "Todos los derechos reservados")
