"""Landing page moderna y responsive para el dashboard."""

# ======================================================
# IMPORTS
# ======================================================
from typing import Final

import streamlit as st

# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ======================================================
# CONSTANTS
# ======================================================
FEATURES: Final[list[dict[str, str]]] = [
    {
        "icon": "📊",
        "title": "Dashboard Interactivo",
        "description": (
            "Métricas clave y gráficos dinámicos " "filtrables por período y categoría."
        ),
    },
    {
        "icon": "🔐",
        "title": "Autenticación Segura",
        "description": (
            "Sistema de usuarios con registro, " "login y recuperación de contraseña."
        ),
    },
    {
        "icon": "⚡",
        "title": "Datos en Tiempo Real",
        "description": (
            "Visualizaciones rápidas y datos " "actualizados dinámicamente."
        ),
    },
]

CUSTOM_CSS: Final[
    str
] = """
<style>

/* ======================================================
   GLOBAL
====================================================== */

.main {
    padding-top: 2rem;
}

/* ======================================================
   HERO SECTION
====================================================== */

.hero-container {
    text-align: center;
    padding: 4rem 1rem 3rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: #111827;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #6B7280;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.8;
}

/* ======================================================
   FEATURE CARDS
====================================================== */

.feature-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease-in-out;
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: #111827;
}

.feature-description {
    font-size: 1rem;
    color: #6B7280;
    line-height: 1.7;
}

/* ======================================================
   CTA BUTTON
====================================================== */

.cta-container {
    padding: 2rem 0;
}

/* ======================================================
   FOOTER
====================================================== */

.footer {
    text-align: center;
    color: #9CA3AF;
    padding: 2rem 0 1rem;
    font-size: 0.9rem;
}

</style>
"""


# ======================================================
# HELPER FUNCTIONS
# ======================================================
def render_feature_card(
    icon: str,
    title: str,
    description: str,
) -> None:
    """Renderiza una tarjeta de funcionalidad."""

    st.markdown(
        f"""
        <div class="feature-card">

            <div class="feature-icon">
                {icon}
            </div>

            <div class="feature-title">
                {title}
            </div>

            <div class="feature-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_section() -> None:
    """Renderiza la sección principal."""

    st.markdown(
        """
        <div class="hero-container">

            <h1 class="hero-title">
                Gestión Inteligente de Ventas
            </h1>

            <p class="hero-subtitle">
                Visualiza métricas, analiza tendencias
                y toma decisiones estratégicas con
                datos en tiempo real.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cta_button() -> None:
    """Renderiza el botón principal."""

    _, center_col, _ = st.columns([1, 1, 1])

    with center_col:
        login_clicked = st.button(
            "🔐 Iniciar Sesión",
            type="primary",
            use_container_width=True,
        )

        if login_clicked:
            st.switch_page("pages/2_login.py")


def render_features_section() -> None:
    """Renderiza las funcionalidades principales."""

    st.subheader("✨ Funcionalidades principales")

    columns = st.columns(len(FEATURES))

    for column, feature in zip(columns, FEATURES):
        with column:
            render_feature_card(
                icon=feature["icon"],
                title=feature["title"],
                description=feature["description"],
            )


def render_footer() -> None:
    """Renderiza el footer."""

    st.markdown(
        """
        <div class="footer">
            © 2026 · Dashboard de Ventas ·
            Todos los derechos reservados
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# APP INITIALIZATION
# ======================================================
st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True,
)

# ======================================================
# PAGE CONTENT
# ======================================================
render_hero_section()

st.markdown(
    '<div class="cta-container">',
    unsafe_allow_html=True,
)

render_cta_button()

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

render_features_section()

st.divider()

render_footer()
