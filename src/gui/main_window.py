import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional
from .canvas import StarMapCanvas
from .route_controller import RouteController
from .research_config_panel import ResearchConfigPanel
from ..models.graphBase import graphBase
from ..utils.json_loader import load_constellations
from ..models.star_graph import StarGraph
from ..models.donkey import Donkey
from .simulation_state_panel import SimulationStatePanel
from .simulation_controller import SimulationController

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
        self.root.geometry("900x1100")  # Aumentado de 950 a 1100
        self.root.configure(bg="#1a1a1a")

        # Datos cargados inicialmente (inicia con None)
        self.star_map = None
        self.constellations = None
        self.burro_data = None
        self.graph = None
        
        # Controladores (se inicializarán después de crear widgets)
        self.route_controller = None
        self.research_config_panel = None
        self.simulation_state_panel = None
        self.simulation_controller = None

        #Crear interfaz
        self._create_widgets()

    def _create_widgets(self):
        """Crea los widgets de la interfaz."""
        
        # Crear canvas principal con scrollbar para toda la ventana
        main_canvas = tk.Canvas(self.root, bg="#1a1a1a")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#1a1a1a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Usar scrollable_frame como contenedor principal
        container = scrollable_frame

        # Header con título
        header_frame = tk.Frame(container, bg="#2c3e50", height=60)
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
        control_frame = tk.Frame(container, bg="#34495e", height=50)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        #Guardar referencia a control_frame
        self.control_frame = control_frame

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
        canvas_frame = tk.Frame(container, bg="#1a1a1a")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        #Crear el canvas del mapa estelar
        self.canvas = StarMapCanvas(canvas_frame, width=850, height=500)
        self.canvas.pack()

        # -----------------------
        # Nuevo: frame para los controles de simulación
        # Se mostrará justo debajo del canvas (visible mientras se ejecuta)
        self.sim_controls_frame = tk.Frame(container, bg="#34495e")
        self.sim_controls_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        # -----------------------

        # Frame para paneles de requisitos (Req 2 y Req 3)
        requirements_frame = tk.Frame(container, bg="#34495e")
        requirements_frame.pack(fill=tk.X, padx=10, pady=5)

        
        # Crear controlador de rutas (Requisito 2)
        self.route_controller = RouteController(requirements_frame, self.canvas, self.status_label)

        # Crear panel de estado del burro (Requisito 3)
        self.simulation_state_panel = SimulationStatePanel(container)

        # Crear controlador de simulación (Requisito 3)
        # Se inicializará con datos después de cargar JSON
        self.simulation_controller = None  # Se creará después
        
        # Crear panel de configuración de investigación (Requisito 3)
        # Se inicializa con star_map vacío, se cargará después
        self.research_config_panel = None  # Se creará después de cargar JSON

        # PANEL DE INFORMACIÓN
        info_frame = tk.Frame(container, bg="#2c3e50", height=100)
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

        self.info_label.pack(pady=10)

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
        self.root.update()

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
        
        self.canvas.highlight_blocked_edges(StarGraph(self.graph, self.star_map))

        
        # Actualizar información
        self._update_info_panel()

                # Crear StarGraph y Donkey para pasar al RouteController
        # Crear StarGraph y Donkey para pasar al RouteController
        star_graph = StarGraph(self.graph, self.star_map)

        # 🔧 Panel de Control de Caminos
        from .path_control_panel import PathControlPanel
        self.path_control_panel = PathControlPanel(self.route_controller.parent_frame, self.canvas, star_graph)
        self.path_control_panel.pack(fill=tk.X, padx=10, pady=10)

        donkey = Donkey(
            initial_energy=self.burro_data["burroenergiaInicial"],
            health_state=self.burro_data["estadoSalud"],
            grass_kg=self.burro_data["pasto"],
            start_age=self.burro_data["startAge"],
            death_age=self.burro_data["deathAge"]
)

        
        # Pasar datos al controlador de rutas
        self.route_controller.load_data(self.star_map, star_graph, donkey)
        
            
        # Crear controlador de simulación si aún no existe (ahora en sim_controls_frame)
        if self.simulation_controller is None:
            # Usar el frame que está justo debajo del canvas para los controles de simulación
            parent_for_sim = getattr(self, "sim_controls_frame", None)
            if parent_for_sim is None:
                # Fallback: si por alguna razón no existe, usar el requirements_frame
                parent_for_sim = self.route_controller.parent_frame
            self.simulation_controller = SimulationController(
                parent_for_sim,
                self.canvas,
                self.simulation_state_panel,
                self.star_map
            )

        
        # Crear panel de configuración de investigación si aún no existe (DESPUÉS)
        if self.research_config_panel is None:
            # Usar el mismo parent_frame que RouteController
            requirements_frame = self.route_controller.parent_frame
            self.research_config_panel = ResearchConfigPanel(
                requirements_frame, 
                self.star_map,
                self.canvas,  # Pasar el canvas
                self.simulation_controller  # Pasar el controlador de simulación (ya existe)
            )
        
        # Cargar datos en el panel de configuración
        self.research_config_panel.load_data(star_graph, donkey)
        
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
