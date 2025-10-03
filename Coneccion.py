# Coneccion.py
import os
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"), 
    "database": os.getenv("DB_NAME"),
    "auth_plugin": os.getenv("DB_AUTH_PLUGIN", "caching_sha2_password"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "use_pure": True,
    "connection_timeout": 10,
}

_pool = MySQLConnectionPool(pool_name="main_pool", pool_size=5, **DB_CONFIG)

def connection():
    """Obtiene una conexión del pool (debes cerrarla tras usarla)."""
    return _pool.get_connection()

def query_all(sql, params=None, dict_cursor=True):
    """SELECT * -> lista de filas"""
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
    """SELECT una fila"""
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
    """INSERT/UPDATE/DELETE -> filas afectadas"""
    conn = connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            affected = cur.rowcount
        conn.commit()
        return affected
    finally:
        conn.close()

