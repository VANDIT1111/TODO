from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from app.database import Base, SQLALCHEMY_DATABASE_URL
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.models import User, Task  # Ensure models are imported

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

# Set metadata for auto-generating migrations
target_metadata = Base.metadata

# Ensure Alembic gets the correct database URL
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,  # Use url from config
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
