import sqlite3
from pathlib import Path

DATABASE_PATH = Path("business_assistant.db")


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the leads table if it does not exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                company TEXT,
                budget REAL DEFAULT 0,
                urgency TEXT,
                interest_level TEXT,
                notes TEXT,
                score INTEGER DEFAULT 0,
                priority TEXT,
                recommended_action TEXT,
                created TEXT NOT NULL
            )
            """
        )


def add_lead(lead):
    """Save a new lead to the database."""
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO leads (
                name,
                email,
                company,
                budget,
                urgency,
                interest_level,
                notes,
                score,
                priority,
                recommended_action,
                created
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lead["name"],
                lead["email"],
                lead["company"],
                lead["budget"],
                lead["urgency"],
                lead["interest_level"],
                lead["notes"],
                lead["score"],
                lead["priority"],
                lead["recommended_action"],
                lead["created"],
            ),
        )


def get_all_leads():
    """Return all saved leads ordered by score."""
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT *
            FROM leads
            ORDER BY score DESC, id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def delete_lead(lead_id):
    """Delete a lead using its database ID."""
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM leads WHERE id = ?",
            (lead_id,),
        )


def get_lead_statistics():
    """Return basic dashboard statistics."""
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM leads"
        ).fetchone()[0]

        hot = connection.execute(
            """
            SELECT COUNT(*)
            FROM leads
            WHERE priority = 'HOT'
            """
        ).fetchone()[0]

        average = connection.execute(
            """
            SELECT COALESCE(AVG(score), 0)
            FROM leads
            """
        ).fetchone()[0]

    return {
        "total": total,
        "hot": hot,
        "average_score": round(average, 1),
    }
