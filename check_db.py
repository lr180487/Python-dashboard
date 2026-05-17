import sqlite3
import sys

db_path = r"C:\Users\lreyn\CascadeProjects\python-dashboard\dashboard.db"
try:
    c = sqlite3.connect(db_path)
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tablas:", [t[0] for t in tables])
    if ("alembic_version",) in tables:
        versions = c.execute("SELECT version_num FROM alembic_version").fetchall()
        print("Alembic versions:", [v[0] for v in versions])
    else:
        print("No alembic_version table")
except Exception as e:
    print("Error:", e)
    sys.exit(1)
