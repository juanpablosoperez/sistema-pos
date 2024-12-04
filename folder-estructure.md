La mejor práctica es tener una estructura de proyecto organizada. El archivo `pyproject.toml` debería estar en la raíz del proyecto, junto con otros archivos de configuración principales. Aquí te muestro la estructura recomendada:

```
sistema-pos/                  # Carpeta raíz del proyecto
├── pyproject.toml           # Configuración de Poetry y herramientas
├── README.md                # Documentación principal
├── .env                     # Variables de entorno por defecto
├── .env.development         # Variables para desarrollo
├── .env.production          # Variables para producción
├── .gitignore              # Archivos ignorados por git
├── .pre-commit-config.yaml  # Configuración de pre-commit
│
├── sistema_pos/            # Paquete principal (código fuente)
│   ├── __init__.py
│   ├── main.py            # Punto de entrada
│   ├── config.py          # Configuraciones
│   ├── models/            # Modelos de datos
│   ├── views/             # Vistas de Flet
│   └── controllers/       # Lógica de negocio
│
├── tests/                  # Pruebas
│   ├── __init__.py
│   ├── test_models/
│   └── test_controllers/
│
├── scripts/               # Scripts de utilidad
│   ├── __init__.py
│   └── db_setup.py
│
└── migrations/            # Migraciones de Alembic
    └── versions/
```

Para reorganizar tu proyecto actual:

1. Crea la estructura de directorios:

```bash
mkdir -p sistema-pos/sistema_pos/{models,views,controllers}
mkdir -p sistema-pos/{tests,scripts,migrations}
```

2. Mueve el archivo `pyproject.toml` a la raíz:

```bash
mv pyproject.toml sistema-pos/
```

3. Inicia un nuevo repositorio git si aún no lo has hecho:

```bash
cd sistema-pos
git init
```

4. Crea un `.gitignore` básico:

```bash
# .gitignore
__pycache__/
*.py[cod]
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.env*
!.env.example
.venv
.coverage
htmlcov/
```

5. Ajusta tu `main.py` para que funcione con la nueva estructura:

```python
# sistema_pos/main.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Obtener la ruta raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent

def load_environment():
    env_name = os.getenv("ENV_NAME", "development")

    # Cargar .env desde la raíz del proyecto
    default_env = ROOT_DIR / ".env"
    if default_env.exists():
        load_dotenv(default_env)

    env_file = ROOT_DIR / f".env.{env_name}"
    if env_file.exists():
        load_dotenv(env_file, override=True)

def main():
    load_environment()
    # Tu código principal aquí

if __name__ == "__main__":
    main()
```

6. Actualiza las rutas en tu `pyproject.toml`:

```toml
[tool.poe.tasks]
dev = { cmd = "python -m sistema_pos.main", env = { "ENV_NAME" = "development" } }
prod = { cmd = "python -m sistema_pos.main", env = { "ENV_NAME" = "production" } }
```

Para iniciar el proyecto en la nueva estructura:

1. Entra en la carpeta del proyecto:

```bash
cd sistema-pos
```

2. Instala las dependencias:

```bash
poetry install
```

3. Ejecuta en modo desarrollo:

```bash
poetry run poe dev
```

Esta estructura tiene varias ventajas:

- Separación clara de responsabilidades
- Fácil de mantener y escalar
- Sigue las mejores prácticas de Python
- Facilita el testing
- Mejor organización de configuraciones

¿Necesitas ayuda para mover algún código existente a esta nueva estructura?
