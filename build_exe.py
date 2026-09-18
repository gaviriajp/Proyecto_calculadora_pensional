"""
Script para compilar el ejecutable de Windows (.exe) usando PyInstaller y Kivy.
Ejecución:
    python build_exe.py
"""
import os
import sys
import subprocess
import shutil

def compilar():
    print("=" * 60)
    print(" Compilando Calculadora Pensional para Windows...")
    print("=" * 60)

    # Limpiar compilaciones anteriores
    for carpeta in ["build", "dist"]:
        if os.path.exists(carpeta):
            print(f"Limpiando carpeta {carpeta}...")
            shutil.rmtree(carpeta, ignore_errors=True)

    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "CalculadoraPensional.spec"
    ]

    print(f"Ejecutando: {' '.join(comando)}")
    resultado = subprocess.run(comando)

    if resultado.returncode == 0:
        ruta_exe = os.path.abspath(os.path.join("dist", "CalculadoraPensional", "CalculadoraPensional.exe"))
        print("\n" + "=" * 60)
        print(" ¡COMPILACIÓN EXITOSA!")
        print(f" Ejecutable generado en:")
        print(f" {ruta_exe}")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(" ERROR en la compilación con PyInstaller.")
        print("=" * 60)
        sys.exit(resultado.returncode)

if __name__ == "__main__":
    compilar()
