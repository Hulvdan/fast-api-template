import importlib
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

BASE_DIR = Path(__file__).parent.parent.absolute()
sys.path.append(str(BASE_DIR))

from core.config import AppConfig, DatabaseConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
dsn = DatabaseConfig().database_url.replace("+asyncpg", "")
print(dsn)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
# set endpoint from config
config.set_main_option("sqlalchemy.url", dsn)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = []
for app in AppConfig().apps:
    try:
        i = importlib.import_module("apps.{}.models".format(app))
    except ModuleNotFoundError:
        continue

    if len(target_metadata) > 0:
        continue
    elif hasattr(i, "__all__") and len(i.__all__) > 0:
        model = i.__all__[0]
        target_metadata.append(getattr(i, model).metadata)


# target_metadata = [Base.metadata]


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
