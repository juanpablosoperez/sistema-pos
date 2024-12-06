# Sistema de Punto de Venta

Sistema de punto de venta desarrollado con Python, utilizando Flet para la interfaz gráfica y SQLAlchemy para la gestión de base de datos.

## 🚀 Características

- Gestión de inventario
- Sistema de ventas
- Control de compras
- Gestión de proveedores
- Generación de reportes
- Interfaz gráfica moderna
- Base de datos MySQL

## 🛠️ Requisitos Previos

- Python 3.10+
- MySQL Server
- Poetry (Gestor de dependencias)
- Git
- pre-commit

## 🚀 Configuración Inicial

1. Clonar el repositorio:
   ```bash
   git clone <url-repositorio>
   cd sistema-pos
   ```

2. Instalar dependencias:
   ```bash
   poetry install
   ```

3. Configurar pre-commit:
   ```bash
   poetry run pre-commit install
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env.development
   cp .env.example .env.production
   # Editar los archivos con las configuraciones correspondientes
   ```

## 💻 Entornos de Desarrollo

### Desarrollo
```bash
poetry shell  # Activar entorno virtual
poetry run dev  # Ejecutar en modo desarrollo
```

### Producción
```bash
poetry run prod  # Ejecutar en modo producción
```

## 📝 Control de Calidad del Código

### Pre-commit hooks

Los siguientes checks se ejecutan automáticamente antes de cada commit:
- `black`: Formateador de código
- `isort`: Ordenamiento de imports
- `flake8`: Linter de código
- Checks básicos (espacios en blanco, archivos grandes, etc.)

Para ejecutar los hooks manualmente:
```bash
poetry run pre-commit run --all-files
```

### Sistema de Commits

Usamos Commitizen para mantener un formato consistente en los commits:

```bash
# Primero agrega los archivos que quieres commitear
git add archivo1.py archivo2.py

# Luego ejecuta el comando de commit interactivo
poetry run cz commit
```

El comando te guiará paso a paso para crear un commit con el formato correcto:
1. Seleccionar tipo de cambio
2. Escribir descripción corta
3. Agregar descripción larga (opcional)

Tipos de commits disponibles:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato
- `refactor`: Refactorización de código
- `test`: Añadir o modificar tests
- `chore`: Tareas de mantenimiento

## 🗄️ Base de Datos

### Migraciones
```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## 🧪 Testing
```bash
poetry run pytest  # Ejecutar todos los tests
poetry run pytest tests/specific_test.py  # Ejecutar test específico
poetry run pytest -v  # Modo verbose
```

## 📦 Gestión de Dependencias

```bash
# Añadir dependencia
poetry add <paquete>  # para producción
poetry add --group dev <paquete>  # para desarrollo

# Actualizar dependencias
poetry update

# Ver dependencias instaladas
poetry show
```

## 📁 Estructura del Proyecto
```
sistema-pos/
├── alembic/            # Migraciones de base de datos
├── src/                # Código fuente
│   ├── app/           # Aplicación principal
│   ├── config/        # Configuraciones
│   └── utils/         # Utilidades
├── tests/             # Tests
├── .env.development   # Variables de entorno desarrollo
├── .env.production    # Variables de entorno producción
├── .flake8           # Configuración de flake8
├── .pre-commit-config.yaml  # Configuración de pre-commit
├── alembic.ini       # Configuración de alembic
├── pyproject.toml    # Configuración de poetry
└── README.md         # Este archivo
```

## 🤝 Workflow de Desarrollo

1. Crear nueva rama para feature:
   ```bash
   git checkout main
   git pull
   git checkout -b feature/nombre-feature
   ```

2. Desarrollar con buenas prácticas:
   - Escribir tests
   - Seguir estándares de código
   - Documentar cambios importantes

3. Hacer commits:
   ```bash
   git add <archivos>
   poetry run cz commit
   ```

4. Crear Pull Request:
   - Actualizar rama con main antes de crear PR
   - Verificar que los tests pasan
   - Solicitar review

## ⚙️ Configuración de los Entornos

El proyecto utiliza diferentes archivos de entorno:
- `.env.development`: Configuración para desarrollo local
- `.env.production`: Configuración para producción

Variables de entorno necesarias:
```bash
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pos_db
DB_USER=user
DB_PASSWORD=password
```

## 📚 CLI Commands

# Desarrollo
```bash
poetry run poe dev          # Ejecutar en desarrollo
poetry run poe prod         # Ejecutar en producción
```
# Formateo y Linteo
```bash
poetry run poe format       # Formatea el codigo y acomoda los imports
poetry run poe check        # Mismo que anterior pero hace un check del lint
```
# Git y Migraciones
```bash
poetry run poe commit       # Hacer commit
poetry run poe db-migrate   # Actualizar migraciones
poetry run poe db-rollback  # Revertir migración
poetry run poe db-revision     # Nueva revisión de migración
poetry run poe version      # Actualizar versión
```
# Limpieza
```bash
poetry run poe clean        # Limpiar archivos temporales
```
