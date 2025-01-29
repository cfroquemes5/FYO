import sqlite3
from datetime import datetime, timedelta
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp, sp
from kivy.utils import platform
import pandas as pd

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

class MainInterface(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(10), padding=dp(10), **kwargs)
        self.selected_location = ""
        self.selected_route = ""
        self.selected_date = datetime.now().date()
        self.vehicle_btns = {}
        self.occupation_btns = {}
        self.db_path = self.initialize_database()
        
        self.location_routes = {
            "PUENTE GUADUA": ["VARANTE FUNZA", "MANIZALES", "UTICA", "TOCAIMA", "GUADUA-DORADA", 
                            "PARCELAS CHIA", "IMPORAL", "SAN FRANCISCO", "LA CUESTA", "MADRID-VARIANTE", 
                            "MOSQUERA", "MADRID PARQUE", "CHIA-COTA", "MADRID", "FUNZA", "EL ROSAL", 
                            "FACA", "LA VEGA", "TABIO", "SUBACHOQUE", "FUNZA-ZUAME", "PORTAL CL 80", "TERMINAL"],
            "FONTIBON": ["VILLA DIANA", "IBAGUE", "GUADUAS", "CAPARRAPI", "SANTANA", "CARTAGENA", 
                        "CAMBAO", "MARIQUITA", "HONDA", "BBARRANQUILLA", "FREZNO", "MANIZALEZ", 
                        "ZIPACON", "LA FLORIDA", "DORADA"],
            "ATS": ["R1-AV 68", "R2-AV BOYACA", "R3", "R5", "R6", "SOACHA", "SAN ANTONIO", 
                   "MESITAS", "MELGAR", "GIRARDOT", "VIOTA", "TOCAIMA", "IBAGUE", "PEREIRA", 
                   "MANIZALES", "CALI", "FUSAGASUGA", "ESPINAL", "ANAPOIMA", "PURRIFICACION", 
                   "RICAURTE", "POPAYAN", "BOGOTA-TERMINAL"],
            "ATN": ["CHIA", "TOCANCIPA-GANCHANCIPA", "CAJICA", "BRICEÑO", "ZIPA-LA PAZ", 
                   "TOCANCIPA-SUESCA-PARQUE JAME DUQUE", "TABIO-TENJO-CAJICA", "CAJICA-CAPELLANIA-FONTANAR", 
                   "UBATE", "SAMACA-CHOCONTA", "CHIQUINQUIRA-BARBOSA", "SOPO", "SOGAMOSO DIRECTO", 
                   "CHIQUINQUIRA-SANTA SOFIA", "SESQUILE-TOCANCIPA-GACHANCIPA", "TURMEQUE-BRICEÑO-TOCANCIPA", 
                   "MACHETA", "CARTAGENA", "SUESCA-TOCANCIPA-GACHANCIPA-BRICEÑO", "BARBOSA", 
                   "TUNJA-DUITAMA-SOGAMOSO-PAIPA", "SESQUILE-GUATAVITA", "BUCARAMANGA", "YACOPI", 
                   "DUITAMA-SOGAMOSO", "CHIQUINQUIRA-UBATE", "OTANCHE-CHIQUINQUIRA", 
                   "VILLA DE LEIVA-SAMACA", "YOPAL", "VELEZ-BARBOSA", "VILLA PINZON-CHOCOTA", 
                   "GUATEQUE", "PACHO-ZIPA", "CUCUTA", "TUNJA-BARBOSA", "GUATEQUE-TENZA", 
                   "AGUAAZUL-YOPAL", "TUNJA-PAIPA", "BOGOTA PORTAL 170", "TERMINAL"],
            "COTA": ["COTA-CHIA", "COTA-CHIA-PORTALSUBA"],
            "AUTOLLANO": ["CAQUEZA", "VISTA HERMOSA", "VILLAVICENCIO", "GRANADA", 
                         "PUERTO GAITAN", "SANJOSE DEL GUAVIARE", "BOGOTA"],
            "CALERA": ["GUASCA", "CALERA", "CHOCONTA", "CL72", "TERMINAL"]
        }
        
        self.build_ui()

    def build_ui(self):
        # Título
        self.add_widget(Label(text="Sistema de Transporte", 
                            font_size=sp(22),
                            bold=True,
                            size_hint=(1, None), 
                            height=dp(50)))

        # Selectores
        self.location_selector = self.create_selector("Seleccionar ubicación", self.location_routes.keys())
        self.add_widget(self.location_selector)
        
        self.route_selector = self.create_selector("Seleccionar ruta", [])
        self.add_widget(self.route_selector)

        # Ruta personalizada
        self.custom_route = TextInput(
            hint_text="Ingrese nueva ruta",
            multiline=False,
            size_hint=(1, None),
            height=dp(45),
            font_size=sp(16),
            padding=[dp(10), dp(10)]
        )
        self.add_widget(self.custom_route)

        # Tipo de vehículo
        self.add_widget(Label(text="Tipo de vehículo:", 
                            size_hint=(1, None), 
                            height=dp(25),
                            font_size=sp(16)))
        self.add_widget(self.create_button_grid(["C", "M", "BTA", "BC", "BL"], 5))

        # Ocupación
        self.add_widget(Label(text="Ocupación:", 
                            size_hint=(1, None), 
                            height=dp(25),
                            font_size=sp(16)))
        self.add_widget(self.create_button_grid(["A", "B", "C", "D", "E", "F", "V", "P", "ST"], 5))

        # Botones de control
        control_layout = BoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))
        control_layout.add_widget(Button(text="GUARDAR", on_press=self.save_record))
        control_layout.add_widget(Button(text="RESUMEN", on_press=self.show_date_input))
        self.add_widget(control_layout)

        # Botones de datos
        data_layout = BoxLayout(size_hint=(1, None), height=dp(60), spacing=dp(10))
        data_layout.add_widget(Button(text="EXPORTAR", on_press=self.export_data))
        data_layout.add_widget(Button(text="ELIMINAR", on_press=self.confirm_delete))
        self.add_widget(data_layout)

    def create_selector(self, title, options):
        main_button = Button(text=title,
                           size_hint=(1, None),
                           height=dp(45),
                           font_size=sp(16))
        
        dropdown = DropDown()
        for option in options:
            btn = Button(text=option,
                       size_hint_y=None,
                       height=dp(40),
                       font_size=sp(14))
            btn.bind(on_release=lambda b: (dropdown.select(b.text), self.update_route_dropdown()))
            dropdown.add_widget(btn)
        
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        
        if title == "Seleccionar ubicación":
            dropdown.bind(on_select=lambda instance, x: self.set_location(x))
        
        return main_button

    def create_button_grid(self, options, cols):
        grid = GridLayout(cols=cols, spacing=dp(5), size_hint=(1, None), height=dp(80))
        self.buttons_group = {}
        
        for option in options:
            btn = Button(text=option,
                       font_size=sp(16),
                       background_normal='',
                       background_color=(0.9, 0.9, 0.9, 1))
            btn.bind(on_press=self.toggle_button)
            grid.add_widget(btn)
            self.buttons_group[option] = btn
        
        return grid

    def initialize_database(self):
        if platform == 'android':
            from android.storage import app_storage_path
            db_dir = app_storage_path()
        else:
            db_dir = os.getcwd()
        
        db_path = os.path.join(db_dir, 'transport_data.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS registros
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     fecha TEXT,
                     hora TEXT,
                     ubicacion TEXT,
                     ruta TEXT,
                     vehiculos TEXT,
                     ocupacion TEXT)''')
        
        conn.commit()
        conn.close()
        return db_path

    def set_location(self, location):
        self.selected_location = location
        self.update_route_dropdown()

    def update_route_dropdown(self):
        routes = self.location_routes.get(self.selected_location, [])
        self.route_selector.children[0].text = "Seleccionar ruta"
        dropdown = self.route_selector.children[0].__self__
        dropdown.clear_widgets()
        
        for route in routes:
            btn = Button(text=route, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda b: (dropdown.select(b.text), setattr(self.route_selector.children[0], 'text', b.text)))
            dropdown.add_widget(btn)

    def toggle_button(self, instance):
        current_color = instance.background_color
        new_color = (0.2, 0.7, 0.2, 1) if current_color == [0.9, 0.9, 0.9, 1] else [0.9, 0.9, 0.9, 1]
        instance.background_color = new_color

    def save_record(self, instance):
        try:
            if not self.selected_location:
                raise ValueError("Debe seleccionar una ubicación")
            
            ruta = self.custom_route.text if self.custom_route.text else self.route_selector.children[0].text
            if not ruta or ruta == "Seleccionar ruta":
                raise ValueError("Debe seleccionar o ingresar una ruta")
            
            vehiculos = ",".join([btn.text for btn in self.buttons_group.values() if btn.background_color == [0.2, 0.7, 0.2, 1]])
            ocupacion = ",".join([btn.text for btn in self.buttons_group.values() if btn.background_color == [0.2, 0.7, 0.2, 1]])
            
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''INSERT INTO registros 
                        (fecha, hora, ubicacion, ruta, vehiculos, ocupacion)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                    (datetime.now().strftime("%Y-%m-%d"),
                     datetime.now().strftime("%H:%M"),
                     self.selected_location,
                     ruta,
                     vehiculos,
                     ocupacion))
            conn.commit()
            conn.close()
            
            # Reset UI
            for btn in self.buttons_group.values():
                btn.background_color = [0.9, 0.9, 0.9, 1]
            self.custom_route.text = ""
            
            Popup(title="Éxito",
                 content=Label(text="Registro guardado!"),
                 size_hint=(0.8, 0.3)).open()
            
        except Exception as e:
            Popup(title="Error",
                 content=Label(text=str(e)),
                 size_hint=(0.8, 0.3)).open()

    def show_date_input(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        popup = Popup(title="Seleccionar fecha", content=content, size_hint=(0.9, 0.4))
        
        date_input = TextInput(hint_text="AAAA-MM-DD", font_size=sp(18))
        content.add_widget(date_input)
        
        btn_layout = BoxLayout(size_hint=(1, None), height=dp(50))
        btn_layout.add_widget(Button(text="Cancelar", on_press=popup.dismiss))
        btn_layout.add_widget(Button(text="Aceptar", on_press=lambda x: self.handle_date(popup, date_input.text)))
        content.add_widget(btn_layout)
        
        popup.open()

    def handle_date(self, popup, date_str):
        try:
            self.selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            popup.dismiss()
            self.show_hour_selector()
        except ValueError:
            Popup(title="Error",
                 content=Label(text="Formato de fecha inválido"),
                 size_hint=(0.7, 0.3)).open()

    def show_hour_selector(self):
        content = BoxLayout(orientation='vertical')
        popup = Popup(title="Seleccionar hora", content=content, size_hint=(0.8, 0.6))
        
        grid = GridLayout(cols=4, spacing=dp(5))
        for hour in range(24):
            btn = Button(text=f"{hour:02d}:00", font_size=sp(16))
            btn.bind(on_press=lambda x: self.generate_summary(x.text))
            grid.add_widget(btn)
        
        content.add_widget(grid)
        content.add_widget(Button(text="Cancelar", size_hint_y=None, height=dp(40), on_press=popup.dismiss))
        popup.open()

    def generate_summary(self, selected_hour):
        try:
            conn = sqlite3.connect(self.db_path)
            start_time = datetime.strptime(selected_hour, "%H:%M").time()
            end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()
            
            df = pd.read_sql(f"""SELECT * FROM registros 
                              WHERE fecha = '{self.selected_date}' 
                              AND time(hora) BETWEEN time('{start_time}') AND time('{end_time}')""", conn)
            conn.close()
            
            if df.empty:
                raise ValueError("No hay registros para este período")
            
            # Generar estadísticas
            summary = f"Resumen {self.selected_date} {selected_hour}\n\n"
            
            # Vehículos
            vehiculos = df['vehiculos'].str.split(',').explode()
            v_counts = vehiculos.value_counts()
            summary += "Vehículos:\n"
            for v, count in v_counts.items():
                summary += f"{v}: {count} ({count/sum(v_counts)*100:.1f}%)\n"
            
            # Ocupación
            ocupacion = df['ocupacion'].str.split(',').explode()
            o_counts = ocupacion.value_counts()
            summary += "\nOcupación:\n"
            for o, count in o_counts.items():
                summary += f"{o}: {count} ({count/sum(o_counts)*100:.1f}%)\n"
            
            Popup(title="Resumen",
                 content=Label(text=summary, halign='left'),
                 size_hint=(0.95, 0.8)).open()
            
        except Exception as e:
            Popup(title="Error",
                 content=Label(text=str(e)),
                 size_hint=(0.8, 0.3)).open()

    def export_data(self, instance):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql("SELECT * FROM registros", conn)
            conn.close()
            
            if platform == 'android':
                from android.storage import app_storage_path
                export_dir = app_storage_path()
            else:
                export_dir = os.path.expanduser("~")
            
            export_path = os.path.join(export_dir, "reporte_transporte.xlsx")
            df.to_excel(export_path, index=False)
            
            Popup(title="Éxito",
                 content=Label(text=f"Archivo guardado en:\n{export_path}"),
                 size_hint=(0.8, 0.4)).open()
        except Exception as e:
            Popup(title="Error",
                 content=Label(text=str(e)),
                 size_hint=(0.8, 0.3)).open()

    def confirm_delete(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        popup = Popup(title="Confirmar eliminación", content=content, size_hint=(0.8, 0.4))
        
        content.add_widget(Label(text="¿Eliminar TODOS los registros?"))
        
        btn_layout = BoxLayout(size_hint=(1, None), height=dp(50))
        btn_layout.add_widget(Button(text="Cancelar", on_press=popup.dismiss))
        btn_layout.add_widget(Button(text="Eliminar", on_press=lambda x: self.delete_data(popup)))
        content.add_widget(btn_layout)
        
        popup.open()

    def delete_data(self, popup):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM registros")
            conn.commit()
            conn.close()
            
            popup.dismiss()
            Popup(title="Éxito",
                 content=Label(text="Todos los registros han sido eliminados."),
                 size_hint=(0.8, 0.3)).open()
        except Exception as e:
            Popup(title="Error",
                 content=Label(text=str(e)),
                 size_hint=(0.8, 0.3)).open()


class TransportApp(App):
    def build(self):
        return MainInterface()


if __name__ == '__main__':
    TransportApp().run()