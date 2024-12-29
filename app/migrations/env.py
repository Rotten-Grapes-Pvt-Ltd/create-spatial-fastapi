from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from models import Base
from geoalchemy2.admin.dialects.common import _check_spatial_type
from geoalchemy2 import Geometry, Geography, Raster


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def render_item(obj_type, obj, autogen_context):
    """Apply custom rendering for selected items."""
    if obj_type == 'type' and isinstance(obj, (Geometry, Geography, Raster)):
        import_name = obj.__class__.__name__
        autogen_context.imports.add(f"from geoalchemy2 import {import_name}")
        return "%r" % obj

    # default rendering for other objects
    return False

def include_object(object, name, type_, reflected, compare_to):
    # Exclude 'spatial_ref_sys' from migrations
    if type_ == "index":
        if len(object.expressions) == 1:
            try:
                col = object.expressions[0]
                if (
                    _check_spatial_type(col.type, (Geometry, Geography, Raster))
                    and col.type.spatial_index
                ):
                    return False
            except AttributeError:
                pass
    if type_ == "table" and name == "spatial_ref_sys":
        return False
     
    return True

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        render_item=render_item,
        include_object=include_object,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """
    This function is used to execute migrations within an async context.
    """
    context.configure(connection=connection, 
                      target_metadata=target_metadata,
                      render_item=render_item,
                      include_object=include_object,)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
