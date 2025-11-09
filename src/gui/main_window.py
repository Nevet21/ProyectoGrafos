import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional
from .canvas import StarMapCanvas
from ..models.graphBase import graphBase
from ..utils.json_loader import load_constellations

class MainWindow:
    """
    Ventana principal de la aplicación.
    Contiene el canvas, controles y gestiona la carga de datos.
    """

    def __init__(self, root: tk.Tk):
        """
        Inicializa la ventana principal.

        Args:
            root: Ventana raíz de tkinter
        """

        self.root = root
        self.root.title("🌟 NASA - Mapa Estelar de Constelaciones")
        self.root.geometry("900x950")
        self.root.configure(bg="#1a1a1a")

        # Datos cargados inicialmente (inicia con None)
        self.star_map = None
        self.constellations = None
        self.burro_data = None
        self.graph = None

        #Crear interfaz
        self._create_widgets()

    def _create_widgets(self):
        """Crea los widgets de la interfaz."""

        # Header con título
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text= "Proyecto de Grafos - Mapa Estelar de la NASA",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # PANEL DE CONTROLES
        control_frame = tk.Frame(self.root, bg="#34495e", height=50)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Botón para cargar JSON
        self.load_button = tk.Button(
            control_frame,
            text="📂 Cargar JSON",
            command=self.load_json_file,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            padx=20,
            pady=10
        )
        self.load_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Label de estado
        self.status_label = tk.Label(
            control_frame,
            text="📄 Sin archivo cargado",
            font=("Arial", 10),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        # CANVAS PARA EL MAPA
        canvas_frame = tk.Frame(self.root, bg="#1a1a1a")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        #Crear el canvas del mapa estelar
        self.canvas = StarMapCanvas(canvas_frame, width=850, height=700)
        self.canvas.pack()

        info_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        #Título del panel
        info_title = tk.Label(
            info_frame,
            text="Información del Burro y del Mapa",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        info_title.pack(pady=(10,5))

        #Label para mostrar información detallada
        self.info_label = tk.Label(
            info_frame,
            text="Carga un archivo JSON para ver detalles.",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="white",
            justify=tk.LEFT,
            wraplength=850
        )

    def load_json_file(self):
        """Abre un diálogo para seleccionar archivo JSON y carga los datos
        """
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON de constelaciones",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            initialdir="./data"
        )

        # Si el usuario canceló, salir
        if not file_path:
            return
        
        # Actualizar estado
        self.status_label.config(text=f"Cargando archivo: {file_path.split('/')[-1]}...")


        #Intentar cargar el archivo
        try:
            self._load_data_from_file(file_path)
        except Exception as e:
            self._show_error(f"Error al cargar el archivo:\n{str(e)}")

    def _load_data_from_file(self, file_path: str):
        """
        Carga los datos del archivo JSON seleccionado.
        
        Args:
            file_path: Ruta al archivo JSON
        """
        # Crear grafo
        self.graph = graphBase()
        
        # Cargar datos con json_loader
        self.star_map, self.constellations, self.burro_data, self.graph = load_constellations(
            file_path,
            self.graph
        )
        
        # Verificar que se cargaron datos
        if not self.star_map or not self.constellations:
            raise ValueError("El archivo JSON no contiene datos válidos")
        
        # Cargar datos en el canvas
        self.canvas.load_data(self.star_map, self.constellations)
        
        # Dibujar el mapa
        self.canvas.draw_map()
        
        # Actualizar información
        self._update_info_panel()
        
        # Actualizar estado
        filename = file_path.split('/')[-1]
        self.status_label.config(
            text=f"✅ Cargado: {filename}",
            fg="#2ecc71"  # Verde
        )
        
        # Mostrar mensaje de éxito
        messagebox.showinfo(
            "Carga exitosa",
            f"Se cargaron correctamente:\n"
            f"⭐ {len(self.star_map)} estrellas\n"
            f"🌌 {len(self.constellations)} constelaciones"
        )

    def _update_info_panel(self):
        """Actualiza el panel de información con los datos cargados"""
        
        # Contar estrellas compartidas
        shared_count = len([
            s for s in self.star_map.values() 
            if s.get("shared_by_coords", False)
        ])
        
        # Contar hipergigantes
        hyper_count = len([
            s for s in self.star_map.values()
            if s.get("hypergiant", False)
        ])
        
        # Construir texto informativo
        info_text = (
            f"⭐ Estrellas totales: {len(self.star_map)} | "
            f"🌌 Constelaciones: {len(self.constellations)} | "
            f"🔴 Compartidas: {shared_count} | "
            f"💫 Hipergigantes: {hyper_count}\n"
            f"🐴 Burro: {self.burro_data['estadoSalud']} | "
            f"⚡ Energía inicial: {self.burro_data['burroenergiaInicial']}% | "
            f"🌾 Pasto: {self.burro_data['pasto']} kg"
        )
        
        self.info_label.config(text=info_text, fg="white")

    def _show_error(self, message: str):
        """
        Muestra un mensaje de error al usuario.
        
        Args:
            message: Mensaje de error a mostrar
        """
        self.status_label.config(
            text="❌ Error al cargar archivo",
            fg="#e74c3c"  # Rojo
        )
        
        messagebox.showerror(
            "Error",
            message
        )

    def main():
        """Punto de entrada de la aplicación"""
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()


    if __name__ == "__main__":
        main()