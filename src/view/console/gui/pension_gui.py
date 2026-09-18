"""
Archivo puente de retrocompatibilidad.
La interfaz gráfica se encuentra ahora organizada limpiamente en:
    src/view/gui/pension_gui.py
"""
import sys
import os

# Asegura que src/view/gui esté en el path y ejecuta la GUI
RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
RUTA_GUI = os.path.join(RAIZ_PROYECTO, "src", "view", "gui")
if RUTA_GUI not in sys.path:
    sys.path.insert(0, RUTA_GUI)

from pension_gui import PensionApp

if __name__ == "__main__":
    PensionApp().run()