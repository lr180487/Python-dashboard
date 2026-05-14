# run.ps1 - Lanzador limpio para Windows
# Evita crashes de Colorama/Click al detener con Ctrl+C

$env:NO_COLOR = "1"
$env:PYTHONIOENCODING = "utf-8"

streamlit run app.py
