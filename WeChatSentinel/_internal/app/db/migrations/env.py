import os

from alembic import context
from app.core.config import data_directory
from app.core.storage import ensure_private_directory, exclusive_instance
from app.db.engine import open_engine
from app.models.schema_v1 import metadata

connection = context.config.attributes.get("connection")
if context.is_offline_mode():
    raise RuntimeError("Run the migration against a local SQLite database.")
if connection is not None:
    context.configure(connection=connection, target_metadata=metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    directory = data_directory()
    ensure_private_directory(directory, not os.getenv("SENTINEL_DATA_DIR"))
    with exclusive_instance(directory):
        engine = open_engine(directory)
        try:
            with engine.begin() as connection:
                context.configure(connection=connection, target_metadata=metadata)
                with context.begin_transaction():
                    context.run_migrations()
        finally:
            engine.dispose()
