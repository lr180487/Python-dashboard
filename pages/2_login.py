"""Página de autenticación: login, registro y recuperación."""

# ======================================================
# IMPORTS
# ======================================================
import streamlit as st

from auth.auth_manager import get_authenticator, render_forgot_password, render_register

# ======================================================
# CONSTANTS
# ======================================================
DASHBOARD_PAGE = "pages/3_dashboard.py"

# ======================================================
# PAGE STYLES
# ======================================================
CUSTOM_CSS = """
<style>
.auth-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.auth-title {
    text-align: center;
    margin-bottom: 1rem;
}

.auth-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 2rem;
}
</style>
"""


# ======================================================
# HELPERS
# ======================================================
def apply_custom_styles() -> None:
    """Apply custom styles to auth page."""

    st.markdown(
        CUSTOM_CSS,
        unsafe_allow_html=True,
    )


def redirect_if_authenticated() -> None:
    """Redirect authenticated users to dashboard."""

    if st.session_state.get("authentication_status"):
        st.switch_page(DASHBOARD_PAGE)


def render_header() -> None:
    """Render authentication page header."""

    st.markdown(
        """
        <div class="auth-container">

            <h1 class="auth-title">
                🔐 Acceso al Sistema
            </h1>

            <p class="auth-subtitle">
                Inicia sesión para acceder al dashboard
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login(authenticator) -> None:
    """Render login flow."""

    # ==================================================
    # LOGIN SILENCIOSO POR COOKIE
    # ==================================================
    authenticator.login(location="unrendered")

    # ==================================================
    # FORM LOGIN
    # ==================================================
    if not st.session_state.get("authentication_status"):
        authenticator.login(location="main")


def render_auth_status() -> None:
    """Render authentication result messages."""

    authentication_status = st.session_state.get("authentication_status")

    if authentication_status is True:
        render_success_state()

    elif authentication_status is False:
        st.error(" Usuario o contraseña incorrectos")

    elif authentication_status is None:
        st.info("Ingresa tus credenciales para continuar")


def render_success_state() -> None:
    """Render successful authentication state."""

    st.success(" Inicio de sesión exitoso")

    st.balloons()

    if st.button(
        "Ir al Dashboard →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page(DASHBOARD_PAGE)


def render_auth_tabs(
    authenticator,
    credentials,
) -> None:
    """Render register and forgot password tabs."""

    st.divider()

    tab_register, tab_forgot = st.tabs(
        [
            " Registrarse",
            " Recuperar Contraseña",
        ]
    )

    with tab_register:
        render_register(
            authenticator,
            credentials,
        )

    with tab_forgot:
        render_forgot_password(authenticator)


# ======================================================
# MAIN
# ======================================================
def main() -> None:
    """Main authentication page."""

    apply_custom_styles()

    redirect_if_authenticated()

    render_header()

    authenticator, credentials = get_authenticator()

    render_login(authenticator)

    render_auth_status()

    render_auth_tabs(
        authenticator,
        credentials,
    )


# ======================================================
# ENTRYPOINT
# ======================================================
if __name__ == "__main__":
    main()
