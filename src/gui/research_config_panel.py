"""
ResearchConfigPanel - Panel para configurar parámetros de investigación (Requisito 3)
Permite al científico modificar datos de cada estrella antes de calcular la ruta
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
from .editable_treeview import EditableTreeview


class ResearchConfigPanel:
    """
    Panel GUI para configurar los parámetros de investigación de cada estrella.
    Permite modificar: tiempo, energía, efectos de salud y vida.
    """
    
    def __init__(self, parent_frame, star_map, canvas=None, simulation_controller=None):
        """
        Inicializa el panel de configuración.
        
        Args:
            parent_frame: Frame padre donde se creará el panel
            star_map: Diccionario con información de todas las estrellas
            canvas: Canvas donde se dibujará la ruta (opcional)
        """
        self.parent_frame = parent_frame
        self.star_map = star_map
        self.canvas = canvas
        self.simulation_controller = simulation_controller
        
        # Datos para el algoritmo (se cargarán después)
        self.star_graph = None
        self.donkey = None
        
        # Configuración actual {star_id: {params}}
        self.research_config = {}
        
        # Referencias a widgets
        self.config_window = None
        
        # Inicializar configuración por defecto
        self._init_default_config()
        
        # Crear el panel de control
        self._create_panel()
    
    def _init_default_config(self):
        """Inicializa la configuración por defecto para todas las estrellas"""
        for star_id in self.star_map.keys():
            # Obtener el promedio de las distancias de las aristas de esta estrella
            star_data = self.star_map[star_id]
            linked_to = star_data.get("linkedTo", [])
            
            # Calcular promedio de distancias para las aristas
            if linked_to:
                avg_distance = sum(neighbor.get("distance", 0) for neighbor in linked_to) / len(linked_to)
            else:
                avg_distance = 0.0
            
            self.research_config[star_id] = {
                "research_time": 5.0,          # Tiempo de investigación
                "energy_cost_per_time": 1.0,   # Energía por unidad de tiempo
                "health_effect": 0,             # Cambio en salud (-2 a +2)
                "life_effect": 0.0,             # Años luz perdidos por investigación
                "edge_distance": avg_distance   # Distancia promedio de aristas (años luz)
            }
    
    def _create_panel(self):
        """Crea el panel de control en la interfaz"""
        # Frame para el panel de configuración
        self.panel_frame = tk.LabelFrame(
            self.parent_frame,
            text="⚙️ Configuración de Investigación",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10
        )
        self.panel_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Label de instrucciones
        instruction_label = tk.Label(
            self.panel_frame,
            text="Configura los parámetros de investigación para cada estrella:",
            font=("Arial", 9),
            bg="#34495e",
            fg="white"
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Botón para abrir ventana de configuración
        self.config_button = tk.Button(
            self.panel_frame,
            text="🔬 Configurar Parámetros de Investigación",
            command=self.show_config_window,
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.config_button.pack(fill=tk.X, pady=5)
        
        # Botón para calcular ruta óptima
        self.calculate_route_button = tk.Button(
            self.panel_frame,
            text="🚀 Calcular Ruta Óptima",
            command=self._calculate_optimal_route,
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED  # Deshabilitado hasta que se cargue el JSON
        )
        self.calculate_route_button.pack(fill=tk.X, pady=5)

        # Botón para limpiar ruta dibujada
        self.clear_route_button = tk.Button(
            self.panel_frame,
            text="🗑️ Limpiar Ruta",
            command=self._clear_route,
            font=("Arial", 10),
            bg="#e74c3c",  # Rojo
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED  # Deshabilitado hasta calcular una ruta
        )
        self.clear_route_button.pack(fill=tk.X, pady=5)
        
        # Label con resumen de configuración
        self.summary_label = tk.Label(
            self.panel_frame,
            text=self._get_config_summary(),
            font=("Arial", 8),
            bg="#34495e",
            fg="#ecf0f1",
            justify=tk.LEFT
        )
        self.summary_label.pack(anchor=tk.W, pady=(5, 0))
    
    def load_data(self, star_graph, donkey):
        """
        Carga los datos necesarios para calcular la ruta.
        
        Args:
            star_graph: Grafo de estrellas
            donkey: Instancia del burro
        """
        self.star_graph = star_graph
        self.donkey = donkey
        
        # Habilitar el botón de calcular ruta
        self.calculate_route_button.config(state=tk.NORMAL)
    
    def _get_config_summary(self) -> str:
        """
        Genera un resumen de la configuración actual.
        
        Returns:
            String con resumen
        """
        # Contar estrellas con efectos especiales
        positive_health = sum(1 for c in self.research_config.values() if c["health_effect"] > 0)
        negative_health = sum(1 for c in self.research_config.values() if c["health_effect"] < 0)
        positive_life = sum(1 for c in self.research_config.values() if c["life_effect"] < 0)  # Negativo = gana vida
        negative_life = sum(1 for c in self.research_config.values() if c["life_effect"] > 0)  # Positivo = pierde vida
        
        summary = f"📊 Estrellas configuradas: {len(self.research_config)}\n"
        summary += f"   ✨ Mejoran salud: {positive_health} | ⚠️ Empeoran salud: {negative_health}\n"
        summary += f"   💚 Ganan vida: {positive_life} | ❤️ Pierden vida: {negative_life}"
        
        return summary
    
    def get_research_config(self) -> Dict[int, Dict[str, Any]]:
        """
        Retorna la configuración actual de investigación.
        
        Returns:
            Diccionario {star_id: {research_params}}
        """
        return self.research_config.copy()
    
    def show_config_window(self):
        """Muestra ventana emergente con tabla de estrellas para configurar"""
        # Si ya existe una ventana, traerla al frente
        if self.config_window and self.config_window.winfo_exists():
            self.config_window.lift()
            return
        
        # Crear ventana nueva
        self.config_window = tk.Toplevel(self.parent_frame)
        self.config_window.title("🔬 Configuración de Investigación por Estrella")
        self.config_window.geometry("900x600")
        self.config_window.configure(bg="#2c3e50")
        
        # Hacer la ventana modal (bloquea la ventana principal)
        self.config_window.transient(self.parent_frame)
        self.config_window.grab_set()
        
        # Header
        header_frame = tk.Frame(self.config_window, bg="#34495e", height=60)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⚙️ Configuración de Parámetros de Investigación",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Frame para la tabla
        table_frame = tk.Frame(self.config_window, bg="#2c3e50")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear tabla con Treeview y scrollbar
        self._create_config_table(table_frame)
        
        # Frame para botones
        button_frame = tk.Frame(self.config_window, bg="#2c3e50")
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Botón para restaurar valores por defecto
        reset_button = tk.Button(
            button_frame,
            text="🔄 Restaurar Valores por Defecto",
            command=self._reset_to_defaults,
            font=("Arial", 9),
            bg="#e67e22",
            fg="white",
            padx=15,
            pady=5
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Botón para guardar y cerrar
        save_button = tk.Button(
            button_frame,
            text="💾 Guardar y Cerrar",
            command=self._save_and_close,
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Botón para cancelar
        cancel_button = tk.Button(
            button_frame,
            text="❌ Cancelar",
            command=self.config_window.destroy,
            font=("Arial", 9),
            bg="#c0392b",
            fg="white",
            padx=15,
            pady=5
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def _create_config_table(self, parent):
        """
        Crea la tabla editable usando EditableTreeview.
        
        Args:
            parent: Frame padre donde se colocará la tabla
        """
        # Definir columnas: (id, heading, width)
        columns = [
            ("id", "ID", 50),
            ("name", "Estrella", 150),
            ("time", "Tiempo Invest.", 120),
            ("energy_cost", "Energía/Tiempo", 130),
            ("health_effect", "Efecto Salud", 120),
            ("life_effect", "Efecto Vida", 120),
            ("edge_distance", "Distancia Aristas", 140)
        ]
        
        # Columnas editables (no se puede editar ID ni nombre)
        editable_columns = ["time", "energy_cost", "health_effect", "life_effect", "edge_distance"]
        
        # Crear tabla editable
        self.editable_table = EditableTreeview(parent, columns, editable_columns)
        
        # Configurar validación
        self.editable_table.set_validation_callback(self._validate_value)
        
        # Configurar callback de actualización
        self.editable_table.set_update_callback(self._on_cell_updated)
        
        # Llenar con datos
        self._populate_table()
        
        # Label de ayuda
        help_text = (
            "💡 Doble clic en una celda para editarla\n"
            "   • Tiempo: Unidades de tiempo invertidas en investigación\n"
            "   • Energía/Tiempo: % de energía consumida por unidad de tiempo\n"
            "   • Efecto Salud: -2=Muy malo, -1=Malo, 0=Neutral, +1=Bueno, +2=Muy bueno\n"
            "   • Efecto Vida: Años luz perdidos por investigación\n"
            "   • Distancia Aristas: Años luz de viaje (modifica todas las aristas de la estrella)"
        )
        help_label = tk.Label(
            parent,
            text=help_text,
            font=("Arial", 8),
            bg="#2c3e50",
            fg="#95a5a6",
            justify=tk.LEFT
        )
        help_label.pack(pady=(10, 0))
    
    def _populate_table(self):
        """Llena la tabla con los datos actuales de configuración"""
        # Limpiar tabla
        self.editable_table.clear()
        
        # Insertar datos ordenados por ID
        for star_id in sorted(self.research_config.keys()):
            config = self.research_config[star_id]
            star_name = self.star_map[star_id].get("name", f"Star-{star_id}")
            
            # Formatear valores
            values = (
                star_id,
                star_name,
                f"{config['research_time']:.1f}",
                f"{config['energy_cost_per_time']:.1f}",
                config['health_effect'],
                f"{config['life_effect']:.1f}",
                f"{config['edge_distance']:.1f}"
            )
            
            self.editable_table.insert_row(values, tags=(star_id,))
    
    def _validate_value(self, column_id: str, value: str):
        """
        Valida el valor ingresado según el tipo de columna.
        
        Args:
            column_id: ID de la columna
            value: Valor a validar (string)
            
        Returns:
            Valor validado (convertido al tipo correcto)
            
        Raises:
            ValueError: Si el valor no es válido
        """
        if column_id == "health_effect":
            # Debe ser entero entre -2 y +2
            int_value = int(value)
            if int_value < -2 or int_value > 2:
                raise ValueError("El efecto de salud debe estar entre -2 y +2")
            return int_value
        else:
            # Debe ser float
            float_value = float(value)
            
            # Validaciones adicionales
            if column_id in ["time", "energy_cost", "edge_distance"] and float_value < 0:
                raise ValueError("El valor no puede ser negativo")
            
            return float_value
    
    def _on_cell_updated(self, row_id, column_id: str, new_value):
        """
        Callback cuando se actualiza una celda.
        
        Args:
            row_id: ID de la fila
            column_id: ID de la columna
            new_value: Nuevo valor validado
        """
        # Obtener star_id de la primera columna
        row_data = self.editable_table.tree.item(row_id)["values"]
        star_id = row_data[0]
        
        # Mapear column_id a nombre de parámetro en research_config
        param_mapping = {
            "time": "research_time",
            "energy_cost": "energy_cost_per_time",
            "health_effect": "health_effect",
            "life_effect": "life_effect",
            "edge_distance": "edge_distance"
        }
        
        param_name = param_mapping.get(column_id)
        if param_name:
            # Actualizar configuración
            self.research_config[star_id][param_name] = new_value
            
            # Si se cambió la distancia de aristas, actualizar el mapa
            if column_id == "edge_distance" and star_id in self.star_map:
                self._update_edge_distances(star_id, new_value)
            
            # Redibujar el mapa para reflejar los cambios visuales
            if self.canvas:
                self.canvas.draw_map()
    
    def _update_edge_distances(self, star_id: int, edge_distance: float):
        """
        Actualiza las distancias de las aristas conectadas a una estrella
        estableciendo exactamente el valor de edge_distance.
        
        Args:
            star_id: ID de la estrella modificada
            edge_distance: Nuevo valor para las distancias de las aristas
        """
        # Obtener los vecinos de esta estrella
        star_data = self.star_map.get(star_id)
        if not star_data:
            return
        
        linked_to = star_data.get("linkedTo", [])
        
        # Asegurar que la distancia no sea negativa
        new_distance = max(0.1, edge_distance)
        
        # Para cada vecino, actualizar la distancia
        for neighbor in linked_to:
            neighbor_id = neighbor.get("starId")
            if neighbor_id not in self.star_map:
                continue
            
            # Actualizar la distancia en la dirección: star_id -> neighbor_id
            neighbor["distance"] = new_distance
            
            # También actualizar la arista inversa (neighbor_id -> star_id)
            neighbor_star = self.star_map.get(neighbor_id)
            if neighbor_star:
                neighbor_links = neighbor_star.get("linkedTo", [])
                for link in neighbor_links:
                    if link.get("starId") == star_id:
                        link["distance"] = new_distance
                        break
    
    def _calculate_optimal_route(self):
        """Calcula la ruta óptima usando la configuración actual"""
        from tkinter import simpledialog
        from ..algorithms.optimal_route_finder import OptimalRouteFinder

        #Verifica si tenemos los datos necesarios
        if self.star_graph is None or self.donkey is None:
            messagebox.showerror(
                "Error",
                "No se ha cargado un JSON"
            )
            return
        
        # Pedir estrellas de inicio
        star_ids = list(self.star_map.keys())
        star_names = [f"{sid} - {self.star_map[sid]['name']}" for sid in star_ids]

        start_star_input = simpledialog.askstring(
            "Estrella de Inicio",
            f"Ingresa el ID de la estrella inicial:\n\n"
            f"Estrellas disponibles:\n" + "\n".join(star_names[:10]) + "\n..."
        )

        if not start_star_input:
           return  # Cancelado

        try:
            start_star_id = int(start_star_input)
        except ValueError:
            messagebox.showerror("Error", "Debes ingresar un número válido")
            return

        if start_star_id not in star_ids:
            messagebox.showerror("Error", f"La estrella {start_star_id} no existe en el grafo")
            return
        
        # Crear instancia del buscador de rutas
        finder = OptimalRouteFinder(self.star_graph, self.star_map)

        # Calcular la ruta óptima con la configuración
        result = finder.calculate_optimal_route(
            start_star_id,
            self.donkey,
            self.research_config
        )

        # Mostrar resultado
        if result["success"]:
            route_str = " → ".join(map(str, result["route"]))
            
            # Dibujar la ruta en el canvas ANTES de mostrar el mensaje
            if self.canvas:
                self.canvas.draw_route(result["route"])

                # Cargar simulación en el controlador
                if self.simulation_controller:
                    self.simulation_controller.load_simulation(
                        result["simulation_steps"],
                        result["route"],
                        self.star_graph,  # Pasar el grafo
                        self.research_config  # Pasar la configuración
                    )

                # Habilitar botón de limpiar ruta
                self.clear_route_button.config(state=tk.NORMAL)
            
            messagebox.showinfo(
                "✅ Ruta Óptima Encontrada",
                f"Estrellas visitadas: {result['total_stars_visited']}\n"
                f"Ruta: {route_str}\n\n"
                f"Energía gastada: {result['total_energy_spent']:.2f}%\n"
                f"Energía final: {result['final_donkey_state']['energy']:.2f}%\n"
                f"Burro vivo: {'Sí ✅' if result['final_donkey_state']['is_alive'] else 'No ❌'}"
            )
        else:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo calcular la ruta:\n{result['message']}"
            )

    def _clear_route(self):
        """Limpia la ruta dibujada del canvas"""
        if self.canvas:
            self.canvas.clear_route()
            self.clear_route_button.config(state=tk.DISABLED)
            messagebox.showinfo(
                "Ruta Limpiada",
                "La ruta ha sido eliminada del mapa."
            )
    
    def _reset_to_defaults(self):
        """Restaura todos los valores a sus valores por defecto"""
        response = messagebox.askyesno(
            "Confirmar",
            "¿Estás seguro de que quieres restaurar todos los valores por defecto?\n\n"
            "Se perderán los cambios no guardados."
        )
        
        if response:
            self._init_default_config()
            self._populate_table()
            messagebox.showinfo("Completado", "Valores restaurados a los valores por defecto")
    
    def _save_and_close(self):
        """Guarda la configuración y cierra la ventana"""
        # Actualizar el resumen en el panel principal
        self.summary_label.config(text=self._get_config_summary())
        
        messagebox.showinfo(
            "Guardado",
            "Configuración guardada exitosamente.\n\n"
            "Los parámetros se aplicarán al calcular la ruta óptima."
        )
        
        self.config_window.destroy()