import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Determina el entorno y carga el archivo .env correspondiente
environment = os.getenv("ENVIRONMENT", "development")  # Default to 'development' if not set
env_file = f".env.{environment}"  # Use the appropriate .env file based on the environment
load_dotenv(dotenv_path=env_file)  # Cargar el archivo .env correspondiente

# Obtener las variables de entorno
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("DATABASE_NAME")

# Configurar la URL de la base de datos
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Esta es la configuración de Alembic, que proporciona
# acceso a los valores dentro del archivo .ini en uso.
config = context.config

# Interpretar el archivo de configuración para Python logging.
# Esta línea básicamente configura los loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importar los modelos aquí para autogenerar las migraciones
from database.models.base import Base  # Ajusta el import según tu estructura de proyecto

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo 'offline'."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo 'online'."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar las migraciones en el modo adecuado (offline o online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
