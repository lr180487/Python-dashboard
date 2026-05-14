"""Punto de entrada: router principal con navegación multipágina.

Flujo:
  1. Landing  (no autenticado)
  2. Login    (no autenticado)
  3. Dashboard (autenticado)
"""

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

import streamlit as st

from database.init_db import init_database


def main():
    # Inicializar base de datos (tablas + usuarios de ejemplo)
    init_database()

    # Definir páginas
    landing = st.Page("pages/1_landing.py", title="Inicio", icon="🏠")
    login = st.Page("pages/2_login.py", title="Iniciar Sesión", icon="🔐")
    dashboard = st.Page("pages/3_dashboard.py", title="Dashboard", icon="📊")

    # Navegación condicional según estado de autenticación
    if st.session_state.get("authentication_status"):
        pg = st.navigation([dashboard])
    else:
        pg = st.navigation([landing, login])

    pg.run()


if __name__ == "__main__":
    main()
