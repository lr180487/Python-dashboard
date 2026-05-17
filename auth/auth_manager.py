"""Gestión de autenticación con streamlit-authenticator + SQLAlchemy ORM.

PostgreSQL con fallback a SQLite.
"""

import os
from pathlib import Path

import bcrypt
import streamlit as st
import yaml
from yaml.loader import SafeLoader

import streamlit_authenticator as stauth

from database.session import db_session
from database.crud import get_user_by_username, create_user, update_user_password

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def _load_cookie_config():
    """Carga configuración de cookies desde YAML, con override desde env."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=SafeLoader)
    cookie = config["cookie"]
    # Override de la clave secreta desde variable de entorno (más seguro)
    env_key = os.getenv("COOKIE_SECRET")
    if env_key:
        cookie["key"] = env_key
    return cookie


def _build_credentials_from_db():
    """Construye el diccionario de credenciales desde la base de datos."""
    with db_session() as db:
        from database.models import User

        users = db.query(User).all()
        creds = {"usernames": {}}
        for u in users:
            creds["usernames"][u.username] = {
                "email": u.email,
                "failed_login_attempts": u.failed_login_attempts,
                "logged_in": False,
                "name": u.name,
                "password": u.password_hash,
                "roles": u.roles.split(",") if u.roles else ["user"],
            }
        return creds


def get_authenticator():
    """Crea y retorna el objeto Authenticator con credenciales desde la BD.

    Retorna una tupla (authenticator, credentials). El dict credentials es
    mutable: streamlit-authenticator v0.4+ lo modifica en el registro, así que
    podemos leer el password hasheado desde él.
    """
    cookie = _load_cookie_config()
    credentials = _build_credentials_from_db()
    authenticator = stauth.Authenticate(
        credentials,
        cookie["name"],
        cookie["key"],
        cookie["expiry_days"],
    )
    return authenticator, credentials


def save_new_user(username: str, name: str, email: str, password: str, roles: str = "user"):
    """Guarda un nuevo usuario en la base de datos."""
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with db_session() as db:
        create_user(db, username, email, name, password_hash, roles)


def update_password(username: str, new_password: str):
    """Actualiza la contraseña de un usuario en la base de datos."""
    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    with db_session() as db:
        update_user_password(db, username, password_hash)


def render_register(authenticator, credentials, config=None):
    """Renderiza formulario de registro y guarda en la BD."""
    st.subheader("Crear nueva cuenta")
    try:
        email, username, name = authenticator.register_user(
            location="main", captcha=False
        )
        if email and username and name:
            password = credentials["usernames"][username]["password"]
            save_new_user(username, name, email, password)
            st.success("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
    except Exception as e:
        st.error(f"Error en el registro: {e}")


def render_forgot_password(authenticator, config=None):
    """Renderiza formulario de recuperación de contraseña."""
    st.subheader("Recuperar contraseña")
    try:
        username, email, new_password = authenticator.forgot_password(location="main")
        if username and new_password:
            update_password(username, new_password)
            st.success(f"Nueva contraseña generada: {new_password}")
            st.info("Guarda esta contraseña de forma segura.")
    except Exception as e:
        st.error(f"Error en la recuperación: {e}")
