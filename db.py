from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).parent / "estoque.db"


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with closing(connect()) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK (preco >= 0),
                estoque INTEGER NOT NULL CHECK (estoque >= 0),
                estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK (estoque_minimo >= 0)
            )
            """
        )
        columns = {row[1] for row in connection.execute("PRAGMA table_info(produtos)")}
        if "estoque_minimo" not in columns:
            connection.execute(
                "ALTER TABLE produtos ADD COLUMN estoque_minimo INTEGER NOT NULL DEFAULT 5"
            )


def list_products() -> list[sqlite3.Row]:
    with closing(connect()) as connection, connection:
        return connection.execute("SELECT * FROM produtos ORDER BY nome").fetchall()


def create_product(nome: str, categoria: str, preco: float, estoque: int, estoque_minimo: int = 5) -> None:
    with closing(connect()) as connection, connection:
        connection.execute(
            "INSERT INTO produtos (nome, categoria, preco, estoque, estoque_minimo) VALUES (?, ?, ?, ?, ?)",
            (nome, categoria, preco, estoque, estoque_minimo),
        )


def update_stock(product_id: int, estoque: int) -> None:
    with closing(connect()) as connection, connection:
        connection.execute("UPDATE produtos SET estoque = ? WHERE id = ?", (estoque, product_id))


def update_price(product_id: int, preco: float) -> None:
    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")
    with closing(connect()) as connection, connection:
        connection.execute("UPDATE produtos SET preco = ? WHERE id = ?", (preco, product_id))


def search_products(term: str) -> list[sqlite3.Row]:
    with closing(connect()) as connection:
        return connection.execute(
            "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome",
            (f"%{term}%",),
        ).fetchall()


def delete_product(product_id: int) -> None:
    with closing(connect()) as connection, connection:
        connection.execute("DELETE FROM produtos WHERE id = ?", (product_id,))

