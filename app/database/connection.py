# Variables de entorno
import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

environment = os.getenv("ENVIRONMENT", "development")
env_file = f".env.{environment}"

print("\n=== Verificación de conexión a la base de datos ===")
print(f"Intentando cargar archivo: {env_file}")

# Verifica si el archivo existe
if os.path.exists(env_file):
    print(f"Archivo de configuración encontrado: {env_file}")
    load_dotenv(dotenv_path=env_file)
else:
    print(f"ERROR: No se encontró el archivo {env_file}")

print("\nVariables de entorno cargadas:")
print(f"USER: {os.getenv('USER')}")
print(f"PASSWORD: {'*' * len(os.getenv('PASSWORD', ''))}")  # Por seguridad
print(f"HOST: {os.getenv('HOST')}")
print(f"DATABASE_NAME: {os.getenv('DATABASE_NAME')}")

HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# SQLAlchemy
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
print(f"DATABASE_URL: {DATABASE_URL}\n")

engine = create_engine(DATABASE_URL)

# Resto del código igual...
try:
    engine = create_engine(DATABASE_URL)
    # Prueba la conexión
    with engine.connect() as conn:
        print("Conexión a la base de datos exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {str(e)}")
    raise

# Migraciones automáticas con Alembic (opcional)
# Este bloque puede ser opcional y solo para desarrollo. En producción, considera ejecutar las migraciones manualmente.
# from alembic.config import Config
# from alembic import command

# def run_migrations():
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")

# if os.getenv('ENV') != 'production':
#     run_migrations()


# Modelos y gestión del contexto de la base de datos
# from database.models import Base  # Asegúrate de que este import sea correcto

# No llamamos a create_all, ya que las migraciones de Alembic deben manejar esto
# Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """
    Dependency that can be used to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
