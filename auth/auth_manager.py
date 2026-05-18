import os
from pathlib import Path

import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from database.crud import create_user, get_user_by_username, update_user_password
from database.session import db_session

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def _load_cookie_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=SafeLoader)

    cookie = config["cookie"]
    env_key = os.getenv("COOKIE_SECRET")
    if env_key:
        cookie["key"] = env_key

    return cookie


def _build_credentials_from_db() -> dict:
    with db_session() as db:
        from database.models import User

        users = db.query(User).all()
        creds = {"usernames": {}}

        for user in users:
            creds["usernames"][user.username] = {
                "email": user.email,
                "failed_login_attempts": user.failed_login_attempts,
                "logged_in": False,
                "name": user.name,
                "password": user.password_hash,
                "roles": user.roles.split(",") if user.roles else ["user"],
            }

        return creds


def get_authenticator():
    cookie = _load_cookie_config()
    credentials = _build_credentials_from_db()
    authenticator = stauth.Authenticate(
        credentials,
        cookie["name"],
        cookie["key"],
        cookie["expiry_days"],
    )
    return authenticator, credentials


def save_new_user(
    username: str, name: str, email: str, password: str, roles: str = "user"
) -> None:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with db_session() as db:
        create_user(db, username, email, name, password_hash, roles)


def update_password(username: str, new_password: str) -> None:
    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    with db_session() as db:
        update_user_password(db, username, password_hash)


def render_register(authenticator, credentials, config=None) -> None:
    st.subheader("Create new account")
    try:
        email, username, name = authenticator.register_user(
            location="main", captcha=False
        )
        if email and username and name:
            password = credentials["usernames"][username]["password"]
            save_new_user(username, name, email, password)
            st.success("User registered successfully. You can now login.")
    except Exception as e:
        st.error(f"Registration error: {e}")


def render_forgot_password(authenticator, config=None) -> None:
    st.subheader("Recover password")
    try:
        username, email, new_password = authenticator.forgot_password(location="main")
        if username and new_password:
            update_password(username, new_password)
            st.success(f"New password generated: {new_password}")
            st.info("Store this password securely.")
    except Exception as e:
        st.error(f"Recovery error: {e}")
