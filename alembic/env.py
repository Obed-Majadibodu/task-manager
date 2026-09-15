from logging.config import fileConfig
import os

from sqlalchemy import create_engine

from alembic import context
from dotenv import load_dotenv

from backend.database import Base
from backend import models


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

    