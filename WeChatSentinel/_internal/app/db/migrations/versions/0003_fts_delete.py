"""Enable FTS secure deletion when supported by the SQLite runtime."""
import sqlite3

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def set_mode(enabled):
    connection = op.get_bind()
    if sqlite3.sqlite_version_info >= (3, 42, 0) and connection.exec_driver_sql(
        "SELECT 1 FROM sqlite_master WHERE name='message_fts'"
    ).scalar():
        connection.exec_driver_sql("INSERT INTO message_fts(message_fts, rank) VALUES('secure-delete', ?)", (enabled,))


def upgrade():
    set_mode(1)


def downgrade():
    set_mode(0)
