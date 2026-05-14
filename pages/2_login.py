"""Página dedicada de inicio de sesión, registro y recuperación."""

import streamlit as st

from auth.auth_manager import get_authenticator, render_register, render_forgot_password

st.set_page_config(page_title="Iniciar Sesión", page_icon="🔐", layout="centered")

# ── Si ya está autenticado, mandar al dashboard ──
if st.session_state.get("authentication_status"):
    st.switch_page("pages/3_dashboard.py")

st.title("🔐 Acceso al Sistema")

authenticator, credentials = get_authenticator()

# Intentar login silencioso por cookie primero
authenticator.login(location="unrendered")

# Si después del silencioso sigue sin auth, renderizar formulario
if not st.session_state.get("authentication_status"):
    authenticator.login(location="main")

# Leer estado post-submit
authentication_status = st.session_state.get("authentication_status")

if authentication_status is True:
    st.success("¡Inicio de sesión exitoso!")
    st.balloons()
    if st.button("Ir al Dashboard →"):
        st.switch_page("pages/3_dashboard.py")

elif authentication_status is False:
    st.error("Usuario o contraseña incorrectos")

elif authentication_status is None:
    st.info("Ingresa tus credenciales para continuar")

# Tabs para registro / recuperación (visibles siempre para UX)
st.divider()
tab_register, tab_forgot = st.tabs(["📝 Registrarse", "🔑 Recuperar Contraseña"])
with tab_register:
    render_register(authenticator, credentials)
with tab_forgot:
    render_forgot_password(authenticator)
