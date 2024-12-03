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

## ⚙️ Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/punto-venta.git
cd punto-venta
```

2. Instalar Poetry (si no está instalado)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Instalar dependencias
```bash
poetry install
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Inicializar base de datos
```bash
poetry run migrate
poetry run seed
```

## 🚀 Uso

### Iniciar la aplicación
```bash
poetry run start
```

### Ejecutar tests
```bash
poetry run test
```

### Formatear código
```bash
poetry run format
```

## Workflow Diario

1. Actualizar rama main:

```bash

git checkout main

git pull origin main

```

2. Crear rama para nueva feature:

```bash

git checkout -b feature/nombre-feature

```

3. Activar entorno virtual:

```bash

poetry shell

```

4. Desarrollar con formateo automático:

```bash

# Antes de cada commit

poetry run black .

poetry run isort .

poetry run flake8

```

5. Ejecutar tests:

```bash

poetry run pytest

```

6. Actualizar dependencias (cuando sea necesario):

```bash

poetry add <paquete>  # Añadir nueva dependencia

poetry update        # Actualizar todas las dependencias

```

## Pull Requests

1. Actualizar rama con main:

```bash

git checkout main

git pull origin main

git checkout feature/nombre-feature

git rebase main

```

2. Asegurarse que todo funciona:

```bash

poetry install

poetry run pytest

```

3. Push y crear PR:

```bash

git push origin feature/nombre-feature

```

## Convenciones de Commit

Usar commits semánticos:

- feat: Nueva característica

- fix: Corrección de bug

- docs: Documentación

- style: Formateo

- refactor: Refactorización

- test: Tests

- chore: Mantenimiento

Ejemplo:

```bash

git commit -m "feat: añade sistema de autenticación"

```


### Commits
Usar commits semánticos:
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formateo
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

Ejemplo:
```bash
git commit -m "feat: añade sistema de autenticación"
```

## 📁 Estructura del Proyecto
```
punto-de-venta/
├── src/
│   ├── app/
│   │   ├── models/
│   │   ├── views/
│   │   └── controllers/
│   ├── config/
│   ├── database/
│   ├── services/
│   └── utils/
├── tests/
├── pyproject.toml
└── README.md
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Ejecutar tests con coverage
poetry run pytest --cov

# Ejecutar tests específicos
poetry run pytest tests/test_specific.py
```

## 📦 Gestión de Dependencias

### Añadir dependencia
```bash
poetry add <paquete>  # producción
poetry add --group dev <paquete>  # desarrollo
```

### Actualizar dependencias
```bash
poetry update
```
