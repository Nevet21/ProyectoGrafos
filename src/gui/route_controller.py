"""
RouteController - Controlador para gestión de rutas (Requisito 2)
Maneja el cálculo y visualización de rutas de máxima exploración
"""

import tkinter as tk
from tkinter import messagebox, ttk
from ..models.star_graph import StarGraph
from ..models.donkey import Donkey
from ..algorithms.max_exploration import dijkstra_max_exploration


class RouteController:
    """
    Controlador para gestionar el cálculo y visualización de rutas.
    Responsable del Requisito 2: Máxima Exploración.
    """
    
    def __init__(self, parent_frame, canvas, status_label):
        """
        Inicializa el controlador de rutas.
        
        Args:
            parent_frame: Frame padre donde se creará el panel
            canvas: Canvas donde se dibujarán las rutas
            status_label: Label para mostrar el estado
        """
        self.parent_frame = parent_frame
        self.canvas = canvas
        self.status_label = status_label
        
        # Datos
        self.star_map = None
        self.star_graph = None
        self.donkey = None
        self.current_route = None
        
        # Crear el panel de controles
        self._create_panel()
    
    def _create_panel(self):
        """Crea el panel de controles para el Requisito 2"""
        # Frame para Requisito 2
        self.req2_frame = tk.LabelFrame(
            self.parent_frame,
            text="📊 Requisito 2: Máxima Exploración",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10
        )
        self.req2_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Label de instrucciones
        instruction_label = tk.Label(
            self.req2_frame,
            text="Selecciona estrella de inicio:",
            font=("Arial", 9),
            bg="#34495e",
            fg="white"
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Combobox para seleccionar estrella
        self.star_selector_var = tk.StringVar()
        self.star_selector = ttk.Combobox(
            self.req2_frame,
            textvariable=self.star_selector_var,
            state="readonly",
            width=30
        )
        self.star_selector.pack(fill=tk.X, pady=5)
        self.star_selector['values'] = []
        
        # Botón para calcular ruta
        self.calculate_route_btn = tk.Button(
            self.req2_frame,
            text="🔍 Calcular Ruta de Máxima Exploración",
            command=self._calculate_max_exploration,
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.calculate_route_btn.pack(fill=tk.X, pady=5)
        
        # Label para mostrar resultado
        self.route_result_label = tk.Label(
            self.req2_frame,
            text="",
            font=("Arial", 9),
            justify=tk.LEFT,
            bg="#34495e",
            fg="#3498db"
        )
        self.route_result_label.pack(anchor=tk.W, pady=(5, 0))
    
    def load_data(self, star_map, star_graph, donkey):
        """
        Carga los datos necesarios para calcular rutas.
        
        Args:
            star_map: Mapa de estrellas
            star_graph: Grafo de estrellas
            donkey: Burro con parámetros iniciales
        """
        self.star_map = star_map
        self.star_graph = star_graph
        self.donkey = donkey
        
        # Actualizar selector de estrellas
        self._update_star_selector()
        
        # Habilitar botón
        self.calculate_route_btn.config(state=tk.NORMAL)
    
    def _update_star_selector(self):
        """Actualiza el combobox con las estrellas disponibles"""
        if not self.star_map:
            return
        
        # Crear lista de opciones: "ID - Nombre"
        star_options = []
        for star_id, star_info in self.star_map.items():
            star_obj = star_info.get("star_object")
            if star_obj:
                option = f"{star_id} - {star_obj.name}"
                star_options.append(option)
        
        # Ordenar por ID
        star_options.sort(key=lambda x: int(x.split(" - ")[0]))
        
        # Actualizar combobox
        self.star_selector['values'] = star_options
        
        # Seleccionar la primera por defecto
        if star_options:
            self.star_selector.current(0)
    
    def _calculate_max_exploration(self):
        """Calcula la ruta de máxima exploración usando Dijkstra modificado"""
        try:
            # Obtener ID de la estrella seleccionada
            selection = self.star_selector_var.get()
            if not selection:
                messagebox.showwarning("Advertencia", "Por favor selecciona una estrella de inicio")
                return
            
            # Extraer el ID (formato: "1 - Alpha1")
            start_star_id = int(selection.split(" - ")[0])
            
            # Actualizar estado
            self.status_label.config(text="⏳ Calculando ruta...")
            self.parent_frame.update()
            
            # Ejecutar el algoritmo
            result = dijkstra_max_exploration(self.star_graph, self.donkey, start_star_id)
            
            if result["success"]:
                # Guardar la ruta
                self.current_route = result["route"]
                
                # Redibujar el mapa y la ruta
                self.canvas.draw_map()
                self._draw_route(result["route"])
                
                # Mostrar información
                info_text = (
                    f"✓ Estrellas visitadas: {result['stars_visited']}\n"
                    f"✓ Distancia total: {result['total_distance']:.2f} años luz\n"
                    f"✓ Edad final: {result['final_age']:.2f} años luz\n"
                    f"✓ Vida restante: {result['remaining_life']:.2f} años luz"
                )
                self.route_result_label.config(text=info_text)
                
                # Actualizar status
                self.status_label.config(
                    text=f"✓ Ruta calculada: {result['stars_visited']} estrellas visitadas"
                )
                
                messagebox.showinfo(
                    "Ruta Calculada",
                    f"Se encontró una ruta que visita {result['stars_visited']} estrellas.\n\n"
                    f"Ruta: {' → '.join(map(str, result['route']))}\n\n"
                    f"Distancia total: {result['total_distance']:.2f} años luz"
                )
            else:
                messagebox.showerror("Error", result.get("message", "No se pudo calcular la ruta"))
                self.status_label.config(text="✗ Error al calcular ruta")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular ruta:\n{str(e)}")
            self.status_label.config(text="✗ Error")
    
    def _draw_route(self, route):
        """Dibuja la ruta calculada en el canvas"""
        if not route or len(route) < 2:
            return
        
        # Dibujar la ruta con líneas gruesas de color azul
        for i in range(len(route) - 1):
            from_star_id = route[i]
            to_star_id = route[i + 1]
            
            # Obtener coordenadas de las estrellas
            from_star_info = self.star_map.get(from_star_id)
            to_star_info = self.star_map.get(to_star_id)
            
            if from_star_info and to_star_info:
                from_coords = from_star_info["coordenates"]
                to_coords = to_star_info["coordenates"]
                
                # Escalar coordenadas
                from_x, from_y = self.canvas._scale_coords(from_coords["x"], from_coords["y"])
                to_x, to_y = self.canvas._scale_coords(to_coords["x"], to_coords["y"])
                
                # Dibujar línea gruesa azul
                self.canvas.create_line(
                    from_x, from_y, to_x, to_y,
                    fill="#2196F3",
                    width=4,
                    arrow=tk.LAST,
                    arrowshape=(10, 12, 5),
                    tags="route"
                )
        
        # Resaltar estrella de inicio con círculo verde
        start_id = route[0]
        start_info = self.star_map.get(start_id)
        if start_info:
            coords = start_info["coordenates"]
            x, y = self.canvas._scale_coords(coords["x"], coords["y"])
            self.canvas.create_oval(
                x - 15, y - 15, x + 15, y + 15,
                outline="#4CAF50",
                width=3,
                tags="route"
            )
            self.canvas.create_text(
                x, y - 25,
                text="INICIO",
                font=("Arial", 10, "bold"),
                fill="#4CAF50",
                tags="route"
            )
        
        # Resaltar estrella final con círculo rojo
        end_id = route[-1]
        end_info = self.star_map.get(end_id)
        if end_info:
            coords = end_info["coordenates"]
            x, y = self.canvas._scale_coords(coords["x"], coords["y"])
            self.canvas.create_oval(
                x - 15, y - 15, x + 15, y + 15,
                outline="#F44336",
                width=3,
                tags="route"
            )
            self.canvas.create_text(
                x, y + 25,
                text="FIN",
                font=("Arial", 10, "bold"),
                fill="#F44336",
                tags="route"
            )
    
    def clear_route(self):
        """Limpia la ruta actual del canvas"""
        self.canvas.delete("route")
        self.current_route = None
        self.route_result_label.config(text="")
