from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Base

class AlembicMigrationRunner:
    def __init__(self, config, target_metadata):
        self.config = config
        self.target_metadata = target_metadata
        fileConfig(self.config.config_file_name)

    def run_migrations_offline(self):
        context.configure(
            url=self.config.get_main_option("sqlalchemy.url"),
            target_metadata=self.target_metadata,
            literal_binds=True,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online(self):
        connectable = engine_from_config(
            self.config.get_section(self.config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=self.target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()

    def run(self):
        if context.is_offline_mode():
            self.run_migrations_offline()
        else:
            self.run_migrations_online()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

target_metadata = Base.metadata

if __name__ == "__main__":
    runner = AlembicMigrationRunner(config, target_metadata)
    runner.run()
else:
    runner = AlembicMigrationRunner(config, target_metadata)
    runner.run()
