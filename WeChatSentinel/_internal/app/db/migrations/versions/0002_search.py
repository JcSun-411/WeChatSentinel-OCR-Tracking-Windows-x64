"""Add an optional synchronized trigram index."""
from alembic import op
from sqlalchemy.exc import OperationalError

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    try:
        connection.exec_driver_sql(
            "CREATE VIRTUAL TABLE message_fts USING fts5(content, content='messages', content_rowid='id', tokenize='trigram')"
        )
    except OperationalError as error:
        if not any(token in str(error.orig).lower() for token in ("no such module", "no such tokenizer")):
            raise
        return
    op.execute("INSERT INTO message_fts(message_fts) VALUES('rebuild')")
    op.execute("""CREATE TRIGGER message_fts_insert AFTER INSERT ON messages BEGIN
        INSERT INTO message_fts(rowid, content) VALUES (new.id, new.content);
    END""")
    op.execute("""CREATE TRIGGER message_fts_delete AFTER DELETE ON messages BEGIN
        INSERT INTO message_fts(message_fts, rowid, content) VALUES ('delete', old.id, old.content);
    END""")
    op.execute("""CREATE TRIGGER message_fts_update AFTER UPDATE OF content ON messages BEGIN
        INSERT INTO message_fts(message_fts, rowid, content) VALUES ('delete', old.id, old.content);
        INSERT INTO message_fts(rowid, content) VALUES (new.id, new.content);
    END""")


def downgrade():
    for kind in ("insert", "delete", "update"):
        op.execute(f"DROP TRIGGER IF EXISTS message_fts_{kind}")
    op.execute("DROP TABLE IF EXISTS message_fts")
