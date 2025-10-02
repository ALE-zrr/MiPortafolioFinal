import os
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from pathlib import Path
from dotenv import load_dotenv, find_dotenv, dotenv_values

paths = [
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent / ".env",
    Path.cwd() / ".env",
]
dotenv_path = next((p for p in paths if p.exists()), None) or find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path, override=True, encoding="utf-8-sig")
    print("Cargando .env desde:", dotenv_path)
    print("ENV leídas:", {k: "✓" for k in dotenv_values(dotenv_path, encoding="utf-8-sig").keys()})
else:
    print("No se encontró .env")

def _getenv(name, default=None):
    v = os.getenv(name)
    return v if v not in (None, "", "None") else default

def _require(name: str) -> str:
    v = os.getenv(name)
    if v is None or str(v).strip() == "":
        raise RuntimeError(f"Falta la variable de entorno {name} en tu .env")
    return v

DB_CONFIG = {
    "host": _require("DB_HOST"),
    "port": int(_require("DB_PORT")),
    "user": _require("DB_USER"),
    "password": _require("DB_PASSWORD"),
    "database": _require("DB_NAME"),
    "auth_plugin": _getenv("DB_AUTH_PLUGIN", "caching_sha2_password"),
    "charset": _getenv("DB_CHARSET", "utf8mb4"),
    "use_pure": True,
    "connection_timeout": int(_getenv("DB_TIMEOUT", "10")),
}

_pool = MySQLConnectionPool(pool_name="main_pool", pool_size=int(_getenv("DB_POOL_SIZE", "5")), **DB_CONFIG)

def connection():
    conn = _pool.get_connection()
    collation = _getenv("DB_COLLATION", "utf8mb4_spanish_ci")
    with conn.cursor() as cur:
        cur.execute(f"SET NAMES {DB_CONFIG['charset']} COLLATE {collation};")
    return conn

def query_all(sql, params=None, dict_cursor=True):
    conn = connection()
    try:
        with conn.cursor(dictionary=dict_cursor) as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()

def query_one(sql, params=None, dict_cursor=True):
    conn = connection()
    try:
        with conn.cursor(dictionary=dict_cursor) as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
        conn.commit()
        return row
    finally:
        conn.close()

def execute(sql, params=None):
    conn = connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            affected = cur.rowcount
        conn.commit()
        return affected
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        cn = connection()
        with cn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            print("✅ Conexión OK. MySQL versión:", cur.fetchone()[0])
        cn.close()
    except Exception as e:
        print("❌ Error:", e)
