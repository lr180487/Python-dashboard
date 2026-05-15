<<<<<<< HEAD
# Dashboard de Ventas

Dashboard interactivo construido con Streamlit para visualizar métricas de ventas.

## Estructura del Proyecto

```
python-dashboard/
├── app.py                 # Punto de entrada
├── dashboard.py           # Versión monolítica original (legacy)
├── requirements.txt       # Dependencias
├── README.md              # Documentación
├── data/
│   ├── __init__.py
│   └── generator.py       # Generación de datos sintéticos
├── components/
│   ├── __init__.py
│   ├── metrics.py         # Métricas principales
│   └── charts.py          # Gráficos con Plotly
└── utils/
    ├── __init__.py
    ├── config.py          # Configuración global
    └── filters.py         # Utilidades de filtrado
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Características

- Métricas principales en tiempo real
- Filtros por período y categoría
- Gráfico de pastel (ventas por categoría)
- Gráfico de línea (tendencia diaria)
- Tabla de datos detallados
=======
# Python-dashboard
>>>>>>> 5ffa398284413b837d8982882ffce6c346e3be32
