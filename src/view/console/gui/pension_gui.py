import sys
import os

# Este archivo vive en src/view/console/gui/pension_gui.py, es decir,
# tres carpetas por debajo de 'src' (gui -> console -> view -> src).
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from model import logica_pension


class PensionApp(App):

    def build(self):
        self.title = "Calculadora de Pensión de Vejez"

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


if __name__ == "__main__":
    PensionApp().run()