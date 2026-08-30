import json
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


# Databáze je běhový stav aplikace uložený mimo verzované zdrojové soubory.
DATABASE_PATH = Path(__file__).parent / "data" / "mail_assistant.db"


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Otevře databázovou transakci a po použití připojení bezpečně zavře."""

    # Složka vznikne automaticky až při prvním použití databáze.
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Řádky lze číst podle názvů sloupců, například row["id"].
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    """Vytvoří tabulky potřebné pro úkoly, audit a návrhy zlepšení."""

    with get_connection() as connection:
        # CREATE TABLE IF NOT EXISTS umožňuje bezpečné opakované spuštění.
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id TEXT UNIQUE,
                company TEXT,
                contact_person TEXT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                action TEXT NOT NULL,
                tool_name TEXT,
                success INTEGER NOT NULL,
                details_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS improvement_proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capability TEXT NOT NULL,
                reason TEXT NOT NULL,
                evidence_count INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                approved_at TEXT
            );
            """
        )


def record_audit_event(
    *,
    run_id: str,
    event_type: str,
    action: str,
    success: bool,
    details: dict[str, Any],
    tool_name: str | None = None,
) -> int:
    """Uloží auditní událost bez citlivého obsahu e-mailu."""

    with get_connection() as connection:
        # ensure_ascii=False zachová české znaky v čitelné podobě.
        details_json = json.dumps(details, ensure_ascii=False)

        # Parametrizovaný INSERT odděluje auditní data od SQL příkazu.
        cursor = connection.execute(
            """
            INSERT INTO audit_events (
                run_id,
                event_type,
                action,
                tool_name,
                success,
                details_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                event_type,
                action,
                tool_name,
                int(success),
                details_json,
            ),
        )

        return int(cursor.lastrowid)