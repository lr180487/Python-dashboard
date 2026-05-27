"""
=========================================================
🚀 MAIN APPLICATION ENTRY POINT
=========================================================

Aplicación multipágina con Streamlit.

Flujo:
    1. Landing Page
    2. Login
    3. Dashboard autenticado
"""

# =========================================================
# 📦 STANDARD LIBRARY
# =========================================================
from pathlib import Path

from dotenv import load_dotenv

# =========================================================
# 🌎 THIRD-PARTY IMPORTS
# =========================================================
import streamlit as st

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
# ⚙️ STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="Python Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 🔐 SESSION STATE DEFAULTS
# =========================================================
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = False

if "db_initialized" not in st.session_state:
    st.session_state.db_initialized = False

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
# 🔐 AUTHENTICATION
# =========================================================
def is_authenticated() -> bool:
    """Check authentication status."""

    return bool(
        st.session_state.get(
            "authentication_status",
            False,
        )
    )


# =========================================================
# 🧭 NAVIGATION
# =========================================================
def create_navigation():
    """Create dynamic navigation."""

    pages = PRIVATE_PAGES if is_authenticated() else PUBLIC_PAGES

    return st.navigation(pages)


# =========================================================
# 🗄️ INITIALIZE APP
# =========================================================
def initialize_app() -> None:
    """Initialize application once."""

    if not st.session_state.db_initialized:
        init_database()

        st.session_state.db_initialized = True


# =========================================================
# 🚀 MAIN
# =========================================================
def main() -> None:
    """Main entrypoint."""

    initialize_app()

    navigation = create_navigation()

    navigation.run()


# =========================================================
# ▶️ ENTRYPOINT
# =========================================================
if __name__ == "__main__":
    main()
