import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from test_app.models import *
from user_app.models import *

from quiz_project.conf import Settings
from quiz_project.behaviours.base_model import AbstractBaseModel

config = context.config
fileConfig(config.config_file_name)

target_metadata = AbstractBaseModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = Settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    alembic_config = config.get_section(config.config_ini_section)
    alembic_config['sqlalchemy.url'] = Settings.DATABASE_URL
    connectable = AsyncEngine(
        engine_from_config(
            alembic_config,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
