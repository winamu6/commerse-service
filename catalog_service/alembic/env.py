import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.db.settings import settings
from src.db.database import Base
from src import models
from src.models import product

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata



def run_migrations_offline():
    url = settings.DATABASE_URL_asyncpg
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(
        settings.DATABASE_URL_asyncpg.replace("+asyncpg", ""),
        poolclass=pool.NullPool )
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()