"""
SimulationStatePanel - Panel para mostrar el estado del burro durante la simulación
"""

import tkinter as tk
from tkinter import ttk

class SimulationStatePanel:
    """
    Panel que muestra el estado actual del burro durante la simulación.
    """
    
    def __init__(self, parent_frame):
        """
        Inicializa el panel de estado.
        
        Args:
            parent_frame: Frame padre donde se creará el panel
        """
        self.parent_frame = parent_frame
        self._create_panel()
    
    def _create_panel(self):
        """Crea el panel de estado"""
        # Frame principal
        self.state_frame = tk.LabelFrame(
            self.parent_frame,
            text="🐴 Estado del Burro",
            font=("Arial", 10, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=15,
            pady=10
        )
        self.state_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Grid para organizar los datos
        info_frame = tk.Frame(self.state_frame, bg="#2c3e50")
        info_frame.pack(fill=tk.X)
        
        # Fila 1: Energía y Salud
        tk.Label(
            info_frame, text="⚡ Energía:", 
            font=("Arial", 9, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.energy_label = tk.Label(
            info_frame, text="100.0%", 
            font=("Arial", 9), bg="#2c3e50", fg="#2ecc71"
        )
        self.energy_label.grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(
            info_frame, text="❤️ Salud:", 
            font=("Arial", 9, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).grid(row=0, column=2, sticky="w", padx=(0, 5))
        
        self.health_label = tk.Label(
            info_frame, text="Excelente", 
            font=("Arial", 9), bg="#2c3e50", fg="#2ecc71"
        )
        self.health_label.grid(row=0, column=3, sticky="w")
        
        # Fila 2: Vida y Pasto
        tk.Label(
            info_frame, text="🕐 Vida:", 
            font=("Arial", 9, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(5, 0))
        
        self.life_label = tk.Label(
            info_frame, text="100 / 200 años", 
            font=("Arial", 9), bg="#2c3e50", fg="#3498db"
        )
        self.life_label.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=(5, 0))
        
        tk.Label(
            info_frame, text="🌾 Pasto:", 
            font=("Arial", 9, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(5, 0))
        
        self.grass_label = tk.Label(
            info_frame, text="300 kg", 
            font=("Arial", 9), bg="#2c3e50", fg="#f39c12"
        )
        self.grass_label.grid(row=1, column=3, sticky="w", pady=(5, 0))
        
        # Fila 3: Estrella actual
        tk.Label(
            info_frame, text="⭐ Estrella:", 
            font=("Arial", 9, "bold"), bg="#2c3e50", fg="#ecf0f1"
        ).grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(5, 0))
        
        self.current_star_label = tk.Label(
            info_frame, text="Ninguna", 
            font=("Arial", 9), bg="#2c3e50", fg="#9b59b6"
        )
        self.current_star_label.grid(row=2, column=1, columnspan=3, sticky="w", pady=(5, 0))
        
        # Barra de progreso de energía
        tk.Label(
            self.state_frame, text="Energía:", 
            font=("Arial", 8), bg="#2c3e50", fg="#95a5a6"
        ).pack(anchor="w", pady=(10, 0))
        
        self.energy_bar = ttk.Progressbar(
            self.state_frame, 
            length=300, 
            mode='determinate',
            maximum=100
        )
        self.energy_bar.pack(fill=tk.X, pady=(2, 5))
        self.energy_bar['value'] = 100
        
        # Frame destacado para ubicación actual (NUEVO)
        location_frame = tk.Frame(self.state_frame, bg="#9b59b6", relief=tk.RAISED, borderwidth=2)
        location_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            location_frame,
            text="📍 Ubicación Actual:",
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=8)
        
        self.location_label = tk.Label(
            location_frame,
            text="En tránsito...",
            font=("Arial", 10, "bold"),
            bg="#9b59b6",
            fg="#ecf0f1"
        )
        self.location_label.pack(side=tk.LEFT, padx=5, pady=8)
    
    def update_state(self, donkey_state: dict, current_star_id: int = None, star_map: dict = None):
        """
        Actualiza el panel con el estado actual del burro.
        
        Args:
            donkey_state: Diccionario con el estado del burro
            current_star_id: ID de la estrella actual (opcional)
            star_map: Mapa de estrellas para obtener nombres (opcional)
        """
        # Actualizar energía
        energy = donkey_state.get('energy', 0)
        self.energy_label.config(text=f"{energy:.1f}%")
        self.energy_bar['value'] = energy
        
        # Color según nivel de energía
        if energy > 70:
            energy_color = "#2ecc71"  # Verde
        elif energy > 30:
            energy_color = "#f39c12"  # Naranja
        else:
            energy_color = "#e74c3c"  # Rojo
        self.energy_label.config(fg=energy_color)
        
        # Actualizar salud
        health = donkey_state.get('health_state', 'Desconocido')
        self.health_label.config(text=health)
        
        # Color según salud
        health_colors = {
            'Excelente': '#2ecc71',
            'Regular': '#f39c12',
            'Malo': '#e74c3c'
        }
        self.health_label.config(fg=health_colors.get(health, '#ecf0f1'))
        
        # Actualizar vida
        current_age = donkey_state.get('current_age', 0)
        death_age = donkey_state.get('death_age', 0)
        remaining = death_age - current_age
        self.life_label.config(text=f"{current_age:.1f} / {death_age} años (quedan {remaining:.1f})")
        
        # Color según vida restante
        if remaining > death_age * 0.5:
            life_color = "#3498db"  # Azul
        elif remaining > death_age * 0.2:
            life_color = "#f39c12"  # Naranja
        else:
            life_color = "#e74c3c"  # Rojo
        self.life_label.config(fg=life_color)
        
        # Actualizar pasto
        grass = donkey_state.get('grass_kg', 0)
        self.grass_label.config(text=f"{grass:.1f} kg")
        
        # Actualizar estrella actual
        if current_star_id and star_map and current_star_id in star_map:
            star_name = star_map[current_star_id].get('label', f'Star {current_star_id}')
            self.current_star_label.config(text=f"{current_star_id} - {star_name}")
            # Actualizar ubicación destacada
            self.location_label.config(text=f"Estrella {current_star_id} - {star_name}")
        elif current_star_id:
            self.current_star_label.config(text=f"ID: {current_star_id}")
            self.location_label.config(text=f"Estrella ID: {current_star_id}")
        else:
            self.current_star_label.config(text="Ninguna")
            self.location_label.config(text="En tránsito...")
    
    def reset(self):
        """Resetea el panel a valores por defecto"""
        self.energy_label.config(text="100.0%", fg="#2ecc71")
        self.energy_bar['value'] = 100
        self.health_label.config(text="Excelente", fg="#2ecc71")
        self.life_label.config(text="0 / 0 años", fg="#3498db")
        self.grass_label.config(text="0 kg")
        self.current_star_label.config(text="Ninguna")
        self.location_label.config(text="En tránsito...")