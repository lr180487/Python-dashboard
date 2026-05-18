"""Landing page moderna y responsive para el dashboard."""

# ======================================================
# IMPORTS
# ======================================================
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
FEATURES = [
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
        "title": "Tiempo Real",
        "description": (
            "Visualizaciones rápidas y datos " "actualizados dinámicamente."
        ),
    },
]

CUSTOM_CSS = """
<style>

    /* ==================================================
       GLOBAL
    ================================================== */

    .main {
        padding-top: 2rem;
    }

    /* ==================================================
       HERO SECTION
    ================================================== */

    .hero-container {
        text-align: center;
        padding: 4rem 1rem 3rem 1rem;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #111827;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.8;
    }

    /* ==================================================
       FEATURE CARDS
    ================================================== */

    .feature-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        border: 1px solid #e5e7eb;
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
        color: #6b7280;
        line-height: 1.7;
    }

    /* ==================================================
       FOOTER
    ================================================== */

    .footer {
        text-align: center;
        color: #9ca3af;
        padding: 2rem 0 1rem 0;
        font-size: 0.9rem;
    }

</style>
"""


# ======================================================
# HELPER FUNCTIONS
# ======================================================
def render_feature_card(icon: str, title: str, description: str) -> None:
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


# ======================================================
# APPLY CUSTOM CSS
# ======================================================
st.markdown(
    CUSTOM_CSS,
    unsafe_allow_html=True,
)

# ======================================================
# HERO SECTION
# ======================================================
st.markdown(
    """
    <div class="hero-container">

        <h1 class="hero-title">
            Gestión Inteligente de Ventas
        </h1>

        <p class="hero-subtitle">
            Visualiza métricas, analiza tendencias y toma
            decisiones estratégicas con datos en tiempo real.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# CTA BUTTON
# ======================================================
_, center_col, _ = st.columns([1, 1, 1])

with center_col:
    login_clicked = st.button(
        "🔐 Iniciar Sesión",
        type="primary",
        use_container_width=True,
    )

    if login_clicked:
        st.switch_page("pages/2_login.py")

st.divider()

# ======================================================
# FEATURES SECTION
# ======================================================
st.subheader("✨ Funcionalidades principales")

columns = st.columns(3)

for column, feature in zip(columns, FEATURES):
    with column:
        render_feature_card(
            icon=feature["icon"],
            title=feature["title"],
            description=feature["description"],
        )

# ======================================================
# FOOTER
# ======================================================
st.divider()

st.markdown(
    """
    <div class="footer">
        © 2026 · Dashboard de Ventas ·
        Todos los derechos reservados
    </div>
    """,
    unsafe_allow_html=True,
)
