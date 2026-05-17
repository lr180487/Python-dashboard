#!/usr/bin/env python3
"""
detect_imports.py

Escanea un proyecto Python y genera requirements.in
basado en imports reales (top-level).
"""

import ast
import os
from pathlib import Path

# Mapeo de módulos → paquetes pip (puedes ampliarlo)
IMPORT_TO_PACKAGE = {
    "yaml": "pyyaml",
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "psycopg": "psycopg[binary]",
    "cv2": "opencv-python",
}

# módulos estándar de Python (no incluir)
STDLIB = {
    "os",
    "sys",
    "math",
    "json",
    "datetime",
    "re",
    "subprocess",
    "pathlib",
    "itertools",
    "collections",
    "typing",
    "threading",
    "asyncio",
    "logging",
    "functools",
    "random",
    "time",
}


def extract_imports(file_path):
    """Extrae imports de un archivo Python usando AST."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def scan_project(directory):
    """Escanea todos los .py del proyecto."""
    all_imports = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    all_imports.update(extract_imports(path))
                except Exception:
                    pass  # ignora archivos problemáticos

    return all_imports


def clean_imports(imports):
    """Filtra stdlib y convierte nombres."""
    result = set()

    for imp in imports:
        if imp in STDLIB:
            continue

        package = IMPORT_TO_PACKAGE.get(imp, imp)
        result.add(package)

    return sorted(result)


def generate_requirements_in(packages, output="requirements.in"):
    """Genera el archivo requirements.in"""
    with open(output, "w", encoding="utf-8") as f:
        for pkg in packages:
            f.write(pkg + "\n")

    print(f"✔ requirements.in generado con {len(packages)} paquetes")


if __name__ == "__main__":
    project_path = Path(".")  # carpeta actual

    print("🔍 Escaneando proyecto...")
    imports = scan_project(project_path)

    print(f"Imports detectados: {imports}")

    packages = clean_imports(imports)

    print(f"Paquetes finales: {packages}")

    generate_requirements_in(packages)
