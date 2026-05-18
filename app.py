"""
=========================================================
🚀 MAIN APPLICATION ENTRY POINT
=========================================================

Aplicación multipágina con Streamlit.

Flujo de navegación:
    1. Landing Page       → Usuario no autenticado
    2. Login Page         → Usuario no autenticado
    3. Dashboard Page     → Usuario autenticado

Características:
    - Carga automática de variables de entorno
    - Inicialización de base de datos
    - Navegación dinámica basada en autenticación
    - Arquitectura limpia y mantenible
"""

# =========================================================
# 📦 STANDARD LIBRARY
# =========================================================
from pathlib import Path

# =========================================================
# 🌎 THIRD-PARTY IMPORTS
# =========================================================
import streamlit as st
from dotenv import load_dotenv

# =========================================================
# 📂 LOCAL IMPORTS
# =========================================================
from database.init_db import init_database

# =========================================================
# 🌎 ENVIRONMENT VARIABLES
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

# =========================================================
# ⚙️ STREAMLIT CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Python Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 📄 PAGE DEFINITIONS
# =========================================================
LANDING_PAGE = st.Page(
    "pages/1_landing.py",
    title="Inicio",
    icon="🏠",
)

LOGIN_PAGE = st.Page(
    "pages/2_login.py",
    title="Iniciar Sesión",
    icon="🔐",
)

DASHBOARD_PAGE = st.Page(
    "pages/3_dashboard.py",
    title="Dashboard",
    icon="📊",
)

# =========================================================
# 🗂️ PAGE GROUPS
# =========================================================
PUBLIC_PAGES = [
    LANDING_PAGE,
    LOGIN_PAGE,
]

PRIVATE_PAGES = [
    DASHBOARD_PAGE,
]


# =========================================================
# 🔐 AUTHENTICATION HELPER
# =========================================================
def is_authenticated() -> bool:
    """
    Verifica si el usuario está autenticado.

    Returns:
        bool: Estado de autenticación.
    """
    return bool(st.session_state.get("authentication_status"))


# =========================================================
# 🧭 CREATE NAVIGATION
# =========================================================
def create_navigation():
    """
    Genera navegación dinámica según autenticación.

    Returns:
        streamlit.navigation: Navegación activa.
    """
    pages = PRIVATE_PAGES if is_authenticated() else PUBLIC_PAGES
    return st.navigation(pages)


# =========================================================
# 🗄️ INITIALIZE APPLICATION
# =========================================================
def initialize_app() -> None:
    """
    Inicializa componentes principales de la aplicación.
    """
    init_database()


# =========================================================
# 🚀 MAIN APPLICATION
# =========================================================
def main() -> None:
    """
    Punto principal de ejecución.
    """
    initialize_app()

    navigation = create_navigation()
    navigation.run()


# =========================================================
# ▶️ APPLICATION ENTRYPOINT
# =========================================================
if __name__ == "__main__":
    main()
