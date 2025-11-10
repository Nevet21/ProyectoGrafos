"""
HypergigantDialog - Diálogo modal para seleccionar destino desde hipergigante
Permite al usuario elegir manualmente a qué estrella viajar cuando está en una hipergigante
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional


class HypergigantDialog:
    """
    Diálogo modal que se muestra cuando el burro llega a una estrella hipergigante.
    Permite al usuario seleccionar el próximo destino manualmente.
    """
    
    def __init__(self, parent, current_star_id: int, star_map: Dict, 
                 available_neighbors: List[int], donkey_state: Dict,
                 star_graph=None, research_config: Dict = None):
        """
        Inicializa el diálogo de hipergigante.
        
        Args:
            parent: Ventana padre
            current_star_id: ID de la estrella hipergigante actual
            star_map: Diccionario con información de todas las estrellas
            available_neighbors: Lista de IDs de estrellas vecinas disponibles
            donkey_state: Estado actual del burro
            star_graph: Grafo de estrellas (para calcular mejor ruta)
            research_config: Configuración de investigación actual
        """
        self.parent = parent
        self.current_star_id = current_star_id
        self.star_map = star_map
        self.available_neighbors = available_neighbors
        self.donkey_state = donkey_state
        self.star_graph = star_graph
        self.research_config = research_config or {}
        
        # Variable para almacenar la selección
        self.selected_star_id = None
        self.suggested_route = None
        
        # Crear ventana modal
        self._create_dialog()
    
    def _create_dialog(self):
        """Crea la ventana modal del diálogo"""
        # Ventana principal
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🌟 Portal Hipergigante Activado")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg="#1a1a2e")
        
        # Hacer modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        # Header con animación de estrella
        header_frame = tk.Frame(self.dialog, bg="#9b59b6", height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="🌟 ¡PORTAL HIPERGIGANTE ACTIVADO! 🌟",
            font=("Arial", 18, "bold"),
            bg="#9b59b6",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Subtítulo con estrella actual
        current_star = self.star_map.get(self.current_star_id, {})
        subtitle = tk.Label(
            header_frame,
            text=f"Estrella Actual: {self.current_star_id} - {current_star.get('name', 'Desconocida')}",
            font=("Arial", 12),
            bg="#9b59b6",
            fg="#ecf0f1"
        )
        subtitle.pack(pady=5)
        
        # Contenedor principal
        main_container = tk.Frame(self.dialog, bg="#1a1a2e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información del bonus
        bonus_frame = tk.LabelFrame(
            main_container,
            text="💫 Bonus Recibido",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10
        )
        bonus_frame.pack(fill=tk.X, pady=(0, 15))
        
        bonus_text = (
            "✨ Energía recargada: +50% de la energía actual\n"
            "🌾 Pasto duplicado: x2 kilogramos disponibles"
        )
        tk.Label(
            bonus_frame,
            text=bonus_text,
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#2ecc71",
            justify=tk.LEFT
        ).pack()
        
        # Estado actual del burro
        state_frame = tk.LabelFrame(
            main_container,
            text="🐴 Estado Actual del Burro",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10
        )
        state_frame.pack(fill=tk.X, pady=(0, 15))
        
        state_text = (
            f"⚡ Energía: {self.donkey_state.get('energy', 0):.1f}%\n"
            f"❤️ Salud: {self.donkey_state.get('health_state', 'Desconocida')}\n"
            f"🌾 Pasto: {self.donkey_state.get('grass_kg', 0):.1f} kg\n"
            f"🕐 Vida: {self.donkey_state.get('current_age', 0):.1f} / {self.donkey_state.get('death_age', 0)} años"
        )
        tk.Label(
            state_frame,
            text=state_text,
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            justify=tk.LEFT
        ).pack()
        
        # Selección de destino
        selection_frame = tk.LabelFrame(
            main_container,
            text="🎯 Selecciona tu Destino",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10
        )
        selection_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Instrucciones
        tk.Label(
            selection_frame,
            text="Elige una estrella vecina para viajar usando el portal:",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).pack(pady=(0, 10))
        
        # Lista de estrellas vecinas
        list_frame = tk.Frame(selection_frame, bg="#2c3e50")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox con estrellas
        self.star_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg="#34495e",
            fg="white",
            selectbackground="#3498db",
            selectforeground="white",
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.star_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.star_listbox.yview)
        
        # Poblar lista con estrellas vecinas
        for neighbor_id in self.available_neighbors:
            neighbor_data = self.star_map.get(neighbor_id, {})
            star_name = neighbor_data.get('name', 'Sin nombre')
            star_type = neighbor_data.get('type', 'Desconocida')
            display_text = f"⭐ {neighbor_id:3d} - {star_name:20s} ({star_type})"
            self.star_listbox.insert(tk.END, display_text)
        
        # Seleccionar primera estrella por defecto
        if self.available_neighbors:
            self.star_listbox.select_set(0)
        
        # Botones de acción
        button_frame = tk.Frame(main_container, bg="#1a1a2e")
        button_frame.pack(fill=tk.X)
        
        # Botón Calcular Mejor Ruta (NUEVO)
        suggest_button = tk.Button(
            button_frame,
            text="🧭 Sugerir Mejor Ruta",
            command=self._calculate_best_route,
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2"
        )
        suggest_button.pack(fill=tk.X, pady=(0, 5))
        
        # Frame para botones principales
        action_buttons = tk.Frame(button_frame, bg="#1a1a2e")
        action_buttons.pack(fill=tk.X)
        
        # Botón Confirmar
        confirm_button = tk.Button(
            action_buttons,
            text="✅ Viajar a Estrella Seleccionada",
            command=self._confirm_selection,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        confirm_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        # Botón Cancelar (opcional)
        cancel_button = tk.Button(
            action_buttons,
            text="❌ Cancelar",
            command=self._cancel,
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Manejar cierre de ventana
        self.dialog.protocol("WM_DELETE_WINDOW", self._cancel)
    
    def _confirm_selection(self):
        """Confirma la selección del usuario"""
        selection = self.star_listbox.curselection()
        
        if not selection:
            messagebox.showwarning(
                "Sin Selección",
                "Por favor selecciona una estrella destino.",
                parent=self.dialog
            )
            return
        
        # Obtener índice seleccionado
        index = selection[0]
        self.selected_star_id = self.available_neighbors[index]
        
        # Cerrar diálogo
        self.dialog.destroy()
    
    def _cancel(self):
        """Cancela la selección (toma la primera estrella por defecto)"""
        if self.available_neighbors:
            self.selected_star_id = self.available_neighbors[0]
        self.dialog.destroy()
    
    def _calculate_best_route(self):
        """Calcula y muestra la mejor ruta posible desde la hipergigante"""
        if not self.star_graph:
            messagebox.showwarning(
                "Sin Grafo",
                "No se puede calcular la ruta: grafo no disponible.",
                parent=self.dialog
            )
            return
        
        try:
            # Importar con rutas absolutas
            from src.algorithms.optimal_route_finder import OptimalRouteFinder
            from src.models.donkey import Donkey
            
            # Crear un burro clonado con el estado actual
            temp_donkey = Donkey(
                initial_energy=self.donkey_state.get('energy', 100),
                health_state=self.donkey_state.get('health_state', 'Excelente'),
                grass_kg=self.donkey_state.get('grass_kg', 300),
                start_age=self.donkey_state.get('current_age', 12),
                death_age=self.donkey_state.get('death_age', 500)
            )
            temp_donkey.current_age = self.donkey_state.get('current_age', 12)
            
            # Crear finder
            finder = OptimalRouteFinder(self.star_graph, self.star_map)
            
            # Calcular ruta óptima desde la estrella actual
            result = finder.calculate_optimal_route(
                self.current_star_id,
                temp_donkey,
                self.research_config
            )
            
            if result["success"] and result["total_stars_visited"] > 1:
                route = result["route"]
                route_str = " → ".join(map(str, route))
                
                # Mostrar información
                message = (
                    f"🧭 Ruta Sugerida desde aquí:\n\n"
                    f"📍 Ruta: {route_str}\n\n"
                    f"⭐ Estrellas visitables: {result['total_stars_visited']}\n"
                    f"⚡ Energía final: {result['final_donkey_state']['energy']:.1f}%\n"
                    f"❤️ Salud final: {result['final_donkey_state']['health_state']}\n"
                    f"🕐 Vida restante: {result['final_donkey_state']['remaining_life']:.1f} años\n\n"
                    f"¿Deseas viajar a la primera estrella de esta ruta?"
                )
                
                response = messagebox.askyesno(
                    "Ruta Sugerida",
                    message,
                    parent=self.dialog
                )
                
                if response and len(route) > 1:
                    # Seleccionar la primera estrella de la ruta (después de la actual)
                    next_star = route[1]
                    if next_star in self.available_neighbors:
                        index = self.available_neighbors.index(next_star)
                        self.star_listbox.selection_clear(0, tk.END)
                        self.star_listbox.selection_set(index)
                        self.star_listbox.see(index)
            else:
                messagebox.showinfo(
                    "Sin Ruta",
                    "No se encontró una ruta viable desde aquí.\n\n"
                    "El burro no puede continuar sin morir.",
                    parent=self.dialog
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al calcular la ruta:\n{str(e)}",
                parent=self.dialog
            )
    
    def show(self) -> Optional[int]:
        """
        Muestra el diálogo y espera a que el usuario seleccione.
        
        Returns:
            ID de la estrella seleccionada, o None si canceló
        """
        # Esperar a que se cierre el diálogo
        self.dialog.wait_window()
        
        return self.selected_star_id
