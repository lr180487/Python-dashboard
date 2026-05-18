"""Landing page atractiva con CTA hacia login."""

# ======================================================
# IMPORTS
# ======================================================
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
# STYLES
# ======================================================
CUSTOM_CSS = """
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
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

st.divider()


# ======================================================
# FEATURE CARD COMPONENT
# ======================================================
def render_feature_card(
    icon: str,
    title: str,
    description: str,
) -> None:
    """Render reusable feature card."""

    st.markdown(
        f"""
        <div class="feature-card">

            <div class="feature-icon">
                {icon}
            </div>

            <h4>{title}</h4>

            <p>
                {description}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# FEATURES SECTION
# ======================================================
st.subheader("¿Qué puedes hacer?")

c1, c2, c3 = st.columns(3)

with c1:
    render_feature_card(
        "📊",
        "Dashboard Interactivo",
        ("Métricas clave y gráficos dinámicos " "filtrables por período y categoría."),
    )

with c2:
    render_feature_card(
        "🔐",
        "Autenticación Segura",
        ("Sistema de usuarios con registro, " "login y recuperación de contraseña."),
    )

with c3:
    render_feature_card(
        "⚡",
        "Respuesta en Tiempo Real",
        ("Datos generados al vuelo con " "visualizaciones rápidas y responsivas."),
    )

# ======================================================
# FOOTER
# ======================================================
st.divider()

st.caption("© 2026 · Dashboard de Ventas · " "Todos los derechos reservados")
