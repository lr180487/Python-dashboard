# =========================================================
# 🔐 AUTH MANAGER
# =========================================================

import os
from pathlib import Path

import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from database.crud import create_user, update_user_password
from database.session import db_session

# =========================================================
# 📁 CONFIG
# =========================================================

CONFIG_PATH = Path(__file__).parent / "config.yaml"

DEFAULT_ROLE = "user"

# =========================================================
# ⚙️ CONFIG HELPERS
# =========================================================


def load_config() -> dict:
    """
    Load YAML authentication config.
    """

    with open(CONFIG_PATH, encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)


def load_cookie_config() -> dict:
    """
    Load cookie configuration and override
    secret key from environment variables.
    """

    config = load_config()

    cookie_config = config.get("cookie", {}).copy()

    env_secret = os.getenv("COOKIE_SECRET")

    if env_secret:
        cookie_config["key"] = env_secret

    return cookie_config


# =========================================================
# 👤 USER CREDENTIALS
# =========================================================


def build_credentials_from_db() -> dict:
    """
    Build Streamlit-Authenticator credentials
    structure from database users.
    """

    from database.models import User

    credentials = {"usernames": {}}

    with db_session() as db:
        users = db.query(User).all()

        for user in users:
            credentials["usernames"][user.username] = {
                "email": user.email,
                "name": user.name,
                "password": user.password_hash,
                "failed_login_attempts": user.failed_login_attempts,
                "logged_in": False,
                "roles": (user.roles.split(",") if user.roles else [DEFAULT_ROLE]),
            }

    return credentials


# =========================================================
# 🔐 AUTHENTICATOR
# =========================================================


def get_authenticator():
    """
    Create Streamlit Authenticator instance.
    """

    cookie_config = load_cookie_config()

    credentials = build_credentials_from_db()

    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie_config["name"],
        key=cookie_config["key"],
        cookie_expiry_days=cookie_config["expiry_days"],
    )

    return authenticator, credentials


# =========================================================
# 🔒 PASSWORD UTILITIES
# =========================================================


def hash_password(password: str) -> str:
    """
    Hash plain password using bcrypt.
    """

    if password.startswith(("$2a$", "$2b$", "$2y$")) and len(password) == 60:
        return password

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


# =========================================================
# 👤 USER MANAGEMENT
# =========================================================


def save_new_user(
    username: str,
    name: str,
    email: str,
    password: str,
    roles: str = DEFAULT_ROLE,
) -> None:
    """
    Create new user in database.
    """

    password_hash = hash_password(password)

    with db_session() as db:
        create_user(
            db=db,
            username=username,
            email=email,
            name=name,
            password_hash=password_hash,
            roles=roles,
        )


def update_password(
    username: str,
    new_password: str,
) -> None:
    """
    Update user password.
    """

    password_hash = hash_password(new_password)

    with db_session() as db:
        update_user_password(
            db=db,
            username=username,
            password_hash=password_hash,
        )


# =========================================================
# 📝 REGISTER UI
# =========================================================


def render_register(
    authenticator,
    credentials: dict,
) -> None:
    """
    Render registration form.
    """

    st.subheader("Create New Account")

    try:
        email, username, name = authenticator.register_user(
            location="main",
            captcha=False,
        )

        if not all([email, username, name]):
            return

        password = credentials["usernames"][username]["password"]

        save_new_user(
            username=username,
            name=name,
            email=email,
            password=password,
        )

        st.success("User registered successfully. You can now log in.")

    except Exception as error:
        st.error(f"Registration error: {error}")


# =========================================================
# 🔑 PASSWORD RECOVERY UI
# =========================================================


def render_forgot_password(
    authenticator,
) -> None:
    """
    Render forgot password form.
    """

    st.subheader("Recover Password")

    try:
        username, email, new_password = authenticator.forgot_password(
            location="main",
        )

        if not username or not new_password:
            return

        update_password(
            username=username,
            new_password=new_password,
        )

        st.success("New password generated successfully.")

        st.info(f"Temporary password: {new_password}")

    except Exception as error:
        st.error(f"Recovery error: {error}")
