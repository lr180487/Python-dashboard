"""Landing page moderna y responsive."""

# ======================================================
# IMPORTS
# ======================================================
import streamlit as st

# ======================================================
# CSS
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
    height: 100%;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.footer {
    text-align: center;
    color: #888;
    padding-top: 1rem;
}
</style>
"""

# ======================================================
# FEATURES
# ======================================================
FEATURES = [
    {
        "icon": "📊",
        "title": "Dashboard Interactivo",
        "description": (
            "Métricas clave y gráficos dinámicos filtrables por período y categoría."
        ),
    },
    {
        "icon": "🔐",
        "title": "Autenticación Segura",
        "description": ("Sistema de usuarios con registro y login seguro."),
    },
    {
        "icon": "⚡",
        "title": "Tiempo Real",
        "description": ("Visualizaciones rápidas y procesamiento instantáneo."),
    },
]


# ======================================================
# STYLES
# ======================================================
def apply_custom_css() -> None:
    """Apply custom CSS."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ======================================================
# HERO
# ======================================================
def render_hero() -> None:
    """Render hero section."""

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
# CTA
# ======================================================
def render_cta() -> None:
    """Render CTA button."""

    _, center_col, _ = st.columns([1, 1, 1])

    with center_col:
        if st.button(
            "🔐 Iniciar Sesión",
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("pages/2_login.py")


# ======================================================
# FEATURE CARD
# ======================================================
def render_feature_card(
    icon: str,
    title: str,
    description: str,
) -> None:
    """Render feature card."""

    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>

            <h4>{title}</h4>

            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# FEATURES SECTION
# ======================================================
def render_features() -> None:
    """Render features section."""

    st.subheader("¿Qué puedes hacer?")

    cols = st.columns(3)

    for col, feature in zip(cols, FEATURES, strict=False):
        with col:
            render_feature_card(
                feature["icon"],
                feature["title"],
                feature["description"],
            )


# ======================================================
# FOOTER
# ======================================================
def render_footer() -> None:
    """Render footer."""

    st.divider()

    st.markdown(
        """
        <div class="footer">
            © 2026 · Dashboard de Ventas
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# MAIN
# ======================================================
def main() -> None:
    """Main app."""

    apply_custom_css()

    render_hero()

    render_cta()

    st.divider()

    render_features()

    render_footer()


# ======================================================
# ENTRYPOINT
# ======================================================
if __name__ == "__main__":
    main()
