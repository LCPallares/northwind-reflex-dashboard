# 📊 Northwind Analytics Dashboard con Reflex

Un dashboard moderno de inteligencia de negocios construido íntegramente en Python utilizando el framework **Reflex**. Este proyecto visualiza métricas de ventas, inventarios y rendimiento de empleados utilizando la clásica base de datos **Northwind**.

![Reflex Version](img.shields.io)
![Python Version](img.shields.io)
![Database](img.shields.io)

## 🚀 Características

- **Visualización en Tiempo Real:** Gráficos interactivos de ventas mensuales y rendimiento por categoría.
- **Gestión de Inventario:** Tabla dinámica con estados de stock y alertas de reabastecimiento.
- **Buscador Inteligente:** Filtrado rápido de pedidos y clientes con componentes reactivos.
- **UI Moderna:** Interfaz limpia construida con Tailwind CSS y componentes de Radix UI integrados en Reflex.
- **Arquitectura Eficiente:** Backend y Frontend unidos en un solo lenguaje: Python.

## 🛠️ Stack Tecnológico

- **Framework:** [Reflex.dev](reflex.dev)
- **Estilos:** Tailwind CSS (v4)
- **Base de Datos:** Northwind (SQLite)
- **Gráficos:** Reflex Recharts

## 📸 Capturas de Pantalla

A continuación se muestran las vistas principales del dashboard operativo en 2026:

| Dashboard Home (Métricas) | Gestión de Pedidos |
| :--- | :--- |
| ![Dashboard Home](https://i.imgur.com/biDO52E.png) | ![Orders View](https://i.imgur.com/WyZvy5v.png) |



## 📂 Estructura del proyecto
posiblemente se cambie la estructura a futuro para hacerla mas modular

```
📂 northwind-reflex-dashboard
├── 📄 .gitignore               # Archivos ignorados por Git
├── 📂 app                      # Directorio principal de la aplicación
│   ├── 📄 __init__.py
│   ├── 📄 app.py               # Punto de entrada y definición de rutas
│   ├── 📂 components           # Componentes reutilizables de la UI
│   │   ├── 📄 __init__.py
│   │   ├── 📄 charts.py        # Lógica de visualización (Recharts)
│   │   ├── 📄 main_content.py  # Layout principal del dashboard
│   │   └── 📄 sidebar.py       # Navegación lateral
│   ├── 📂 pages                # Vistas específicas de la aplicación
│   │   ├── 📄 __init__.py
│   │   └── 📄 orders.py        # Vista de gestión de pedidos
│   ├── 📄 state.py             # Estado base de la aplicación
│   └── 📂 states               # Lógica de estado modularizada
│       ├── 📄 __init__.py
│       └── 📄 orders_state.py  # Estado y lógica para pedidos
├── 📄 apt-packages.txt         # Dependencias de sistema (para despliegue)
├── 📂 assets                   # Recursos estáticos
│   ├── 📄 __init__.py
│   ├── 📄 favicon.ico
│   └── 📄 placeholder.svg
├── 📄 northwind_schema.txt      # Referencia del esquema SQL
├── 📄 plan.md                  # Roadmap y notas del proyecto
├── 📄 requirements.txt         # Librerías de Python
└── 📄 rxconfig.py              # Configuración principal de Reflex

```

---


## 📦 Instalación

Sigue estos pasos para ejecutar el proyecto localmente en 2026:

1. **Clona el repositorio:**
```bash
git clone github.com
cd northwind-reflex-dashboard
```

2. **Crea un entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

4. **Inicializa y ejecuta:**
```bash
reflex init
reflex run
```

## 🗄️ Configuración de la Base de Datos

El proyecto está configurado para buscar el archivo northwind.db en la raíz. Si deseas usar una base de datos diferente, actualiza la URL en tu archivo rxconfig.py:

```python
config = rx.Config(
    app_name="dashboard",
    db_url="sqlite:///northwind.db",
)
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! 
1. Haz un **Fork** del proyecto.
2. Crea tu rama de función (git checkout -b feature/NuevaMejora).
3. Abre un **Pull Request**.

---

Desarrollado con ❤️ por [Luis Carlos Pallares Ascanio](https://github.com/LCPallares) - 2026.