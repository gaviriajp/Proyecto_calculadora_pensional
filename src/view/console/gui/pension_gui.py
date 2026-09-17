import sys
import os
import csv
from datetime import datetime

# Este archivo vive en src/view/console/gui/pension_gui.py, es decir,
# cuatro carpetas por debajo de la raíz del proyecto
# (gui -> console -> view -> src -> raíz).
RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.append(os.path.join(RAIZ_PROYECTO, "src"))

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from model import logica_pension

# Carpeta 'doc' del proyecto, donde se guarda el historial exportado.
# Se calcula a partir de la ubicación de este archivo (no del directorio
# desde el que se ejecute el programa), para que funcione igual en
# cualquier computador sin importar desde dónde se lance.
CARPETA_DOC = os.path.join(RAIZ_PROYECTO, "doc")
ARCHIVO_HISTORIAL_CSV = os.path.join(CARPETA_DOC, "historial_pensiones.csv")

ENCABEZADOS_CSV = [
    "fecha_hora",
    "ibc_ultimos_10",
    "ibc_toda_vida",
    "salario_minimo_legal",
    "semanas_cotizadas",
    "edad",
    "sexo",
    "ibl",
    "relacion_ibl_smlmv",
    "tasa_base",
    "semanas_adicionales",
    "incremento",
    "tasa_total",
    "pension",
]


class PensionApp(App):

    def build(self):
        self.title = "Calculadora de Pensión de Vejez"

        # Guarda cada cálculo exitoso (datos de entrada + resultado) para
        # poder consultarlo en el historial y exportarlo a CSV.
        self.historial = []

        raiz = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # --- Campos de entrada ---
        campos = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            row_force_default=True,
            row_default_height=40,
        )
        campos.bind(minimum_height=campos.setter("height"))

        campos.add_widget(Label(text="IBC de los últimos 10 años"))
        self.ibc_ultimos_10 = TextInput(text="0", multiline=False)
        campos.add_widget(self.ibc_ultimos_10)

        campos.add_widget(Label(text="IBC de toda la vida laboral"))
        self.ibc_toda_vida = TextInput(text="0", multiline=False)
        campos.add_widget(self.ibc_toda_vida)

        campos.add_widget(Label(text="Salario mínimo legal vigente"))
        self.salario_minimo = TextInput(text="0", multiline=False)
        campos.add_widget(self.salario_minimo)

        campos.add_widget(Label(text="Semanas cotizadas"))
        self.semanas = TextInput(text="0", multiline=False)
        campos.add_widget(self.semanas)

        campos.add_widget(Label(text="Edad"))
        self.edad = TextInput(text="0", multiline=False)
        campos.add_widget(self.edad)

        campos.add_widget(Label(text="Sexo (M/F)"))
        self.sexo = TextInput(text="M", multiline=False)
        campos.add_widget(self.sexo)

        raiz.add_widget(campos)

        # --- Botones ---
        botones = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)

        boton_calcular = Button(text="Calcular Pensión")
        boton_calcular.bind(on_press=self.calcular_pension_gui)
        botones.add_widget(boton_calcular)

        boton_limpiar = Button(text="Limpiar Datos")
        boton_limpiar.bind(on_press=self.limpiar_campos)
        botones.add_widget(boton_limpiar)

        raiz.add_widget(botones)

        # --- Historial / Exportar ---
        botones_historial = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)

        boton_historial = Button(text="Ver Historial")
        boton_historial.bind(on_press=self.mostrar_historial)
        botones_historial.add_widget(boton_historial)

        boton_exportar = Button(text="Exportar CSV")
        boton_exportar.bind(on_press=self.exportar_historial_csv)
        botones_historial.add_widget(boton_exportar)

        raiz.add_widget(botones_historial)

        # --- Resultado ---
        self.resultado = Label(
            text="Aquí va el resultado",
            halign="left",
            valign="top",
        )
        self.resultado.bind(size=self._actualizar_text_size)
        raiz.add_widget(self.resultado)

        return raiz

    def _actualizar_text_size(self, instancia, valor):
        instancia.text_size = valor

    def limpiar_campos(self, sender):
        self.ibc_ultimos_10.text = "0"
        self.ibc_toda_vida.text = "0"
        self.salario_minimo.text = "0"
        self.semanas.text = "0"
        self.edad.text = "0"
        self.sexo.text = "M"
        self.resultado.text = "Aquí va el resultado"

    def mostrar_error(self, mensaje):
        contenido = BoxLayout(orientation="vertical", padding=10, spacing=10)

        etiqueta = Label(text=str(mensaje), halign="center", valign="middle")
        etiqueta.bind(size=self._actualizar_text_size)
        contenido.add_widget(etiqueta)

        cerrar = Button(text="Cerrar", size_hint_y=None, height=40)
        contenido.add_widget(cerrar)

        popup = Popup(
            title="Error de Validación",
            content=contenido,
            size_hint=(None, None),
            size=(450, 250),
        )
        cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def calcular_pension_gui(self, sender):
        # 1. Conversión de los datos ingresados
        try:
            datos = logica_pension.DatosPension(
                ibc_ultimos_10=float(self.ibc_ultimos_10.text),
                ibc_toda_vida=float(self.ibc_toda_vida.text),
                salario_minimo_legal=int(self.salario_minimo.text),
                semanas_cotizadas=int(self.semanas.text),
                edad=int(self.edad.text),
                sexo=self.sexo.text.strip().upper(),
            )
        except ValueError:
            self.mostrar_error("Debe ingresar valores numéricos válidos.")
            return

        # 2. Cálculo (aquí saltan las excepciones propias del modelo)
        try:
            resultado = logica_pension.calcular_pension(datos)
        except Exception as e:
            self.mostrar_error(str(e))
            return

        # 3. Mostrar todos los resultados, igual que la vista de consola
        self.resultado.text = (
            f"IBL calculado: ${resultado.ibl:,.2f}\n"
            f"Salarios mínimos (S): {resultado.relacion:.2f}\n"
            f"Porcentaje base: {resultado.tasa_base:.2f}%\n"
            f"Semanas adicionales: {resultado.semanas_adicionales}\n"
            f"Incremento: {resultado.incremento:.2f}%\n"
            f"Porcentaje total: {resultado.tasa_total:.2f}%\n"
            f"PENSIÓN ESTIMADA: ${resultado.pension:,.2f}"
        )

        # 4. Guardar el cálculo en el historial de la sesión
        self.historial.append(
            {
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "datos": datos,
                "resultado": resultado,
            }
        )

    def mostrar_historial(self, sender):
        """
        Abre una ventana con la lista de todos los cálculos realizados
        durante la sesión actual, del más reciente al más antiguo.
        """
        contenido = BoxLayout(orientation="vertical", padding=10, spacing=10)

        if not self.historial:
            etiqueta_vacio = Label(text="Todavía no has realizado ningún cálculo.")
            contenido.add_widget(etiqueta_vacio)
        else:
            scroll = ScrollView(size_hint=(1, 1))

            lista = BoxLayout(orientation="vertical", size_hint_y=None, spacing=8, padding=5)
            lista.bind(minimum_height=lista.setter("height"))

            for registro in reversed(self.historial):
                datos = registro["datos"]
                resultado = registro["resultado"]

                texto = (
                    f"[b]{registro['fecha_hora']}[/b]\n"
                    f"Edad: {datos.edad}  Sexo: {datos.sexo}  "
                    f"Semanas: {datos.semanas_cotizadas}\n"
                    f"Pensión estimada: ${resultado.pension:,.2f}"
                )

                item = Label(
                    text=texto,
                    markup=True,
                    halign="left",
                    valign="top",
                    size_hint_y=None,
                )
                item.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))
                item.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))
                lista.add_widget(item)

            scroll.add_widget(lista)
            contenido.add_widget(scroll)

        cerrar = Button(text="Cerrar", size_hint_y=None, height=40)
        contenido.add_widget(cerrar)

        popup = Popup(
            title=f"Historial de cálculos ({len(self.historial)})",
            content=contenido,
            size_hint=(0.85, 0.85),
        )
        cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def exportar_historial_csv(self, sender):
        """
        Exporta todo el historial de cálculos de la sesión a un archivo
        CSV, para poder abrirlo luego en Excel o compartirlo.
        """
        if not self.historial:
            self.mostrar_error("No hay cálculos en el historial para exportar todavía.")
            return

        ruta_absoluta = ARCHIVO_HISTORIAL_CSV

        try:
            # Crea la carpeta 'doc' si no existe todavía (por ejemplo, en
            # un computador donde se clonó el repo de forma distinta).
            os.makedirs(CARPETA_DOC, exist_ok=True)

            with open(ruta_absoluta, mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(ENCABEZADOS_CSV)

                for registro in self.historial:
                    datos = registro["datos"]
                    resultado = registro["resultado"]
                    escritor.writerow(
                        [
                            registro["fecha_hora"],
                            datos.ibc_ultimos_10,
                            datos.ibc_toda_vida,
                            datos.salario_minimo_legal,
                            datos.semanas_cotizadas,
                            datos.edad,
                            datos.sexo,
                            f"{resultado.ibl:.2f}",
                            f"{resultado.relacion:.2f}",
                            f"{resultado.tasa_base:.2f}",
                            resultado.semanas_adicionales,
                            f"{resultado.incremento:.2f}",
                            f"{resultado.tasa_total:.2f}",
                            f"{resultado.pension:.2f}",
                        ]
                    )
        except OSError as e:
            # Cubre casos como permisos denegados, disco lleno, ruta
            # inválida en otro computador, etc.
            self.mostrar_error(f"No se pudo guardar el archivo CSV:\n{e}")
            return

        self.mostrar_confirmacion(
            f"Historial exportado correctamente a:\n{ruta_absoluta}"
        )

    def mostrar_confirmacion(self, mensaje):
        contenido = BoxLayout(orientation="vertical", padding=10, spacing=10)

        etiqueta = Label(text=str(mensaje), halign="center", valign="middle")
        etiqueta.bind(size=self._actualizar_text_size)
        contenido.add_widget(etiqueta)

        cerrar = Button(text="Cerrar", size_hint_y=None, height=40)
        contenido.add_widget(cerrar)

        popup = Popup(
            title="Exportación exitosa",
            content=contenido,
            size_hint=(None, None),
            size=(450, 220),
        )
        cerrar.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    PensionApp().run()