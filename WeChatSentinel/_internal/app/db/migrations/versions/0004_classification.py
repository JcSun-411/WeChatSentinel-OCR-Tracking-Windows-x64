"""Cache structured segments with deletion tied to the original message."""
from alembic import op

from app.models.classification import entries, queue

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    entries.create(op.get_bind())
    queue.create(op.get_bind())
    op.get_bind().exec_driver_sql('INSERT INTO classification_queue(message_id) SELECT id FROM messages')
    op.get_bind().exec_driver_sql('''CREATE TRIGGER classification_enqueue AFTER INSERT ON messages BEGIN
        INSERT INTO classification_queue(message_id) VALUES (new.id); END''')


def downgrade():
    op.get_bind().exec_driver_sql('DROP TRIGGER classification_enqueue')
    queue.drop(op.get_bind())
    entries.drop(op.get_bind())
