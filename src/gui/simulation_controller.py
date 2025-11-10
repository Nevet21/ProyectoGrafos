"""
SimulationController - Controlador para simulación paso a paso (Requisito 3)
Permite visualizar el recorrido del burro estrella por estrella
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Any, Optional
import time
from .hypergigant_dialog import HypergigantDialog

class SimulationController:
    """
    Controlador que gestiona la simulación paso a paso de una ruta.
    """

    def __init__(self, parent_frame, canvas, state_panel, star_map):
        """
        Inicializa el controlador de simulación.
        
        Args:
            parent_frame: Frame padre donde se creará el panel
            canvas: Canvas donde se dibuja el mapa
            state_panel: Panel de estado del burro
            star_map: Diccionario con información de las estrellas
        """
        self.parent_frame = parent_frame
        self.canvas = canvas
        self.state_panel = state_panel
        self.star_map = star_map
        
        # Estado de la simulación
        self.simulation_steps = []  # Lista de pasos de la simulación
        self.current_step_index = -1  # Índice del paso actual
        self.is_playing = False  # Si está en modo automático
        self.play_speed = 1000  # Velocidad en ms entre pasos
        
        # Para el diálogo de hipergigante
        self.star_graph = None
        self.research_config = {}
        self.selected_destination = None  # Estrella seleccionada en hipergigante
        
        # Crear el panel de controles
        self._create_panel()
        
        #guardar estrellas 
        self.visited_stars = []  # Para guardar el orden de estrellas visitadas


    def _create_panel(self):
        """Crea el panel de controles de simulación"""
        # Frame principal
        self.sim_frame = tk.LabelFrame(
            self.parent_frame,
            text="🎬 Simulación Paso a Paso",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="white",
            padx=10,
            pady=10
        )
        self.sim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame para botones
        buttons_frame = tk.Frame(self.sim_frame, bg="#34495e")
        buttons_frame.pack(fill=tk.X)
        
        # Botón Iniciar/Reiniciar
        self.start_button = tk.Button(
            buttons_frame,
            text="▶️ Iniciar Simulación",
            command=self._start_simulation,
            font=("Arial", 9, "bold"),
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        # Botón Siguiente Paso
        self.next_button = tk.Button(
            buttons_frame,
            text="⏯️ Siguiente",
            command=self._next_step,
            font=("Arial", 9),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.LEFT, padx=2)
        
        # Botón Automático
        self.play_button = tk.Button(
            buttons_frame,
            text="⏩ Automático",
            command=self._toggle_auto_play,
            font=("Arial", 9),
            bg="#9b59b6",
            fg="white",
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=2)
        
        # Botón Detener
        self.stop_button = tk.Button(
            buttons_frame,
            text="⏹️ Detener",
            command=self._stop_simulation,
            font=("Arial", 9),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=2)
        
        # Label de progreso
        self.progress_label = tk.Label(
            self.sim_frame,
            text="Sin simulación cargada",
            font=("Arial", 9),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.progress_label.pack(pady=(10, 0))

    def load_simulation(self, simulation_steps: List[Dict], route: List[int], 
                       star_graph=None, research_config: Dict = None):
        """
        Carga una simulación para visualizar paso a paso.
        
        Args:
            simulation_steps: Lista de pasos de la simulación
            route: Lista de IDs de estrellas en la ruta
            star_graph: Grafo de estrellas (opcional, para diálogo de hipergigante)
            research_config: Configuración de investigación (opcional)
        """
        self.simulation_steps = simulation_steps
        self.route = route
        self.current_step_index = -1
        self.is_playing = False
        self.selected_destination = None  # Resetear destino seleccionado
        
        # Guardar grafo y configuración para el diálogo
        if star_graph:
            self.star_graph = star_graph
        if research_config:
            self.research_config = research_config
        
        # Habilitar botón de inicio
        self.start_button.config(state=tk.NORMAL)
        self.progress_label.config(
            text=f"Simulación cargada: {len(route)} estrellas, {len(simulation_steps)} pasos"
        )

    def _start_simulation(self):
        """Inicia o reinicia la simulación"""
        # Validar que hay pasos para simular
        if not self.simulation_steps or len(self.simulation_steps) == 0:
            messagebox.showerror(
                "Error",
                "No hay pasos de simulación para visualizar.\n\n"
                "Asegúrate de calcular primero una ruta óptima."
            )
            return
        
        self.current_step_index = -1
        self.is_playing = False
        
        # Limpiar canvas
        self.canvas.clear_route()
        self.canvas.clear_donkey()
        
        # Resetear panel de estado
        self.state_panel.reset()  # Cambiado: state_panel es el nombre correcto
        
        # Habilitar botones
        self.next_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL, text="⏩ Automático")
        self.stop_button.config(state=tk.NORMAL)
        self.start_button.config(text="🔄 Reiniciar")
        
        # Ir al primer paso
        self._next_step()

    def _next_step(self):
        """Avanza al siguiente paso de la simulación"""
        if self.current_step_index >= len(self.simulation_steps) - 1:
            # Simulación terminada
            self._finish_simulation()
            return
        
        # Avanzar al siguiente paso
        self.current_step_index += 1
        step = self.simulation_steps[self.current_step_index]
        
        # Verificar si llegamos al destino seleccionado en hipergigante
        current_star = step.get('star_id')
        if self.selected_destination and current_star == self.selected_destination:
            # Llegamos al destino seleccionado, finalizar simulación
            self._render_step(step)
            self._finish_simulation(custom_message="🎉 ¡Destino alcanzado!")
            return
        
        # Actualizar visualización
        self._render_step(step)
        
        # Actualizar progreso
        self.progress_label.config(
            text=f"Paso {self.current_step_index + 1} / {len(self.simulation_steps)}"
        )
        
        # Si está en modo automático, continuar
        if self.is_playing:
            self.parent_frame.after(self.play_speed, self._next_step)
    
    def _toggle_auto_play(self):
        """Activa/desactiva el modo automático"""
        if not self.is_playing:
            # Iniciar modo automático
            self.is_playing = True
            self.play_button.config(text="⏸️ Pausar", bg="#e67e22")
            self.next_button.config(state=tk.DISABLED)
            self._next_step()
        else:
            # Pausar
            self.is_playing = False
            self.play_button.config(text="⏩ Automático", bg="#9b59b6")
            self.next_button.config(state=tk.NORMAL)
    
    def _stop_simulation(self):
        """Detiene la simulación actual"""
        self.is_playing = False
        self.current_step_index = -1
        
        # Deshabilitar botones
        self.next_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED, text="⏩ Automático", bg="#9b59b6")
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(text="▶️ Iniciar Simulación")
        
        # Limpiar visualización
        self.canvas.clear_donkey()
        
        self.progress_label.config(text="Simulación detenida")
    
    def _finish_simulation(self, custom_message: str = None):
        """Finaliza la simulación
            
        Args:
            custom_message: Mensaje personalizado para mostrar
        """
        self.is_playing = False
        
        # Deshabilitar botones
        self.next_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED, text="⏩ Automático", bg="#9b59b6")
        
        self.progress_label.config(text="✅ Simulación completada")
        
        # 🧩 Validar que hay pasos
        if not self.simulation_steps or len(self.simulation_steps) == 0:
            messagebox.showwarning(
                "Simulación Vacía",
                "No hay información de la simulación."
            )
            # En este caso, no hay nada que reportar, así que terminamos aquí
            return

        # 🧩 Obtener el estado del paso actual o el último
        if self.current_step_index >= 0 and self.current_step_index < len(self.simulation_steps):
            current_step = self.simulation_steps[self.current_step_index]
            donkey_state = current_step.get('donkey_state', {})
        else:
            final_step = self.simulation_steps[-1]
            donkey_state = final_step.get('donkey_state', {})
        
        # 🧩 Mostrar mensaje final según el estado del burro
        if donkey_state.get('is_alive'):
            title = custom_message if custom_message else "✅ Simulación Completada"
            message = f"¡El burro completó la ruta exitosamente!\n\n" if not custom_message else f"{custom_message}\n\n"
            messagebox.showinfo(
                title,
                f"{message}"
                f"Energía final: {donkey_state['energy']:.1f}%\n"
                f"Salud: {donkey_state['health_state']}\n"
                f"Vida restante: {donkey_state['remaining_life']:.1f} años"
            )
        else:
            messagebox.showerror(
                "❌ Burro Fallecido",
                "El burro murió durante el viaje.\n\n"
                "Causa: Edad máxima alcanzada"
            )



        # Obtener el estado del paso actual (si llegamos antes del final)
        if self.current_step_index >= 0 and self.current_step_index < len(self.simulation_steps):
            current_step = self.simulation_steps[self.current_step_index]
            donkey_state = current_step.get('donkey_state', {})
        else:
            # Usar el último paso
            final_step = self.simulation_steps[-1]
            donkey_state = final_step.get('donkey_state', {})
        
        if donkey_state.get('is_alive'):
            title = custom_message if custom_message else "✅ Simulación Completada"
            message = f"¡El burro completó la ruta exitosamente!\n\n" if not custom_message else f"{custom_message}\n\n"
            messagebox.showinfo(
                title,
                f"{message}"
                f"Energía final: {donkey_state['energy']:.1f}%\n"
                f"Salud: {donkey_state['health_state']}\n"
                f"Vida restante: {donkey_state['remaining_life']:.1f} años"
            )
        else:
            messagebox.showerror(
                "❌ Burro Fallecido",
                "El burro murió durante el viaje.\n\n"
                "Causa: Edad máxima alcanzada"
            )
            # 🧩 Mostrar reporte final (se ejecuta siempre que haya pasos)
        self.show_final_report()
        
    def _render_step(self, step: Dict):
        """
        Renderiza un paso de la simulación en el canvas.
        """
        # Obtener datos del paso
        star_id = step.get('star_id')
        donkey_state = step.get('donkey_state', {})
        hypergiant_bonus = step.get('hypergiant_bonus')
        
        # Registrar la estrella visitada
        if star_id and star_id not in self.visited_stars:
            self.visited_stars.append(star_id)

        # Actualizar panel de estado
        self.state_panel.update_state(donkey_state, star_id, self.star_map)

        # 🐴 Movimiento del burro
        if star_id and star_id in self.star_map:
            if len(self.visited_stars) > 1:
                previous_star = self.visited_stars[-2]
                # Animar movimiento suave entre estrellas
                self.canvas.animate_donkey_move(previous_star, star_id)
            else:
                # Primer paso: solo dibujar sin animación
                self.canvas.draw_donkey(star_id)

            # Resaltar la estrella actual
            self.canvas.highlight_star(star_id, color="#ffff00")
        # ✨ Nuevo resaltado aquí

        # Verificar si llegó a una hipergigante
        # Comprobamos tanto por hypergiant_bonus como por la propiedad de la estrella
        star_data = self.star_map.get(star_id, {})
        is_hypergiant = star_data.get('hypergiant', False)

        if is_hypergiant and hypergiant_bonus is not None:
            self._handle_hypergigant(star_id, donkey_state)

    
    def _handle_hypergigant(self, current_star_id: int, donkey_state: Dict):
        """
        Maneja la llegada a una estrella hipergigante.
        Muestra el diálogo para que el usuario elija el destino.
        
        Args:
            current_star_id: ID de la estrella hipergigante
            donkey_state: Estado actual del burro
        """
        # Pausar simulación automática si está activa
        was_playing = self.is_playing
        if self.is_playing:
            self.is_playing = False
            self.play_button.config(text="⏩ Automático", bg="#9b59b6")
            self.next_button.config(state=tk.NORMAL)
        
        # Obtener estrellas vecinas del grafo si está disponible
        available_neighbors = []
        if self.star_graph:
            try:
                neighbors = self.star_graph.get_neighbors(current_star_id)
                available_neighbors = neighbors if neighbors else []
            except:
                pass
        
        # Si no hay grafo o no hay vecinos, usar todas las estrellas
        if not available_neighbors:
            available_neighbors = [sid for sid in self.star_map.keys() if sid != current_star_id]
            available_neighbors = available_neighbors[:10]  # Limitar a 10
        
        # Mostrar diálogo con grafo y configuración
        dialog = HypergigantDialog(
            self.parent_frame,
            current_star_id,
            self.star_map,
            available_neighbors,
            donkey_state,
            self.star_graph,
            self.research_config
        )
        
        selected_star_id = dialog.show()
        
        # Guardar el destino seleccionado
        if selected_star_id:
            self.selected_destination = selected_star_id
            
            # Mostrar mensaje de confirmación
            star_name = self.star_map.get(selected_star_id, {}).get('label', f'Estrella {selected_star_id}')
            messagebox.showinfo(
                "Portal Activado",
                f"🌟 ¡Viajando a {selected_star_id} - {star_name}!\n\n"
                f"El burro ha usado el portal hipergigante.\n"
                f"La simulación continuará hasta llegar al destino seleccionado.",
                parent=self.parent_frame
            )
        
        # Reanudar simulación automática si estaba activa
        if was_playing:
            self.is_playing = True
            self.play_button.config(text="⏸️ Pausar", bg="#e67e22")
            self.next_button.config(state=tk.DISABLED)
        if selected_star_id:
            star_name = self.star_map.get(selected_star_id, {}).get('name', 'Desconocida')
            messagebox.showinfo(
                "Portal Activado",
                f"🌟 ¡Viajando a la estrella {selected_star_id} - {star_name}!\n\n"
                f"El burro ha usado el portal hipergigante.",
                parent=self.parent_frame
            )
        
        # Reanudar simulación automática si estaba activa
        if was_playing:
            self.is_playing = True
            self.play_button.config(text="⏸️ Pausar", bg="#e67e22")
            self.next_button.config(state=tk.DISABLED)
    
    def show_final_report(self):
        """
        Muestra un reporte con las estrellas visitadas, consumo y tiempo.
        """
        if not self.visited_stars:
            messagebox.showinfo("Reporte de Viaje", "No hay estrellas visitadas aún.")
            return

        # Construir texto del reporte
        report_lines = ["📊 REPORTE FINAL DEL VIAJE", ""]

        total_pasto = 0
        total_tiempo = 0

        for star_id in self.visited_stars:
            star = self.star_map.get(star_id, {})
            name = star.get("label", f"Estrella {star_id}")
            constellation = star.get("constellation", "Desconocida")
            time_to_eat = star.get("timeToEat", 0)
            energy = star.get("amountOfEnergy", 0)

            # Simulamos consumo de pasto estimado y tiempo
            pasto_consumido = round(time_to_eat * 1.5, 2)
            tiempo_investigacion = round(time_to_eat * 2, 2)

            total_pasto += pasto_consumido
            total_tiempo += tiempo_investigacion

            report_lines.append(
                f"⭐ {name} ({constellation})"
                f"\n   🌾 Pasto consumido: {pasto_consumido} kg"
                f"\n   ⏱️ Tiempo investigado: {tiempo_investigacion} h"
                f"\n   ⚡ Energía estelar: {energy}%\n"
            )

        report_lines.append(f"-----------------------------------")
        report_lines.append(f"🌾 Pasto total consumido: {total_pasto:.2f} kg")
        report_lines.append(f"⏱️ Tiempo total invertido: {total_tiempo:.2f} h")
        report_lines.append("🐴 Estado final: ver panel lateral")

        # Mostrar reporte en una ventana emergente
        report_text = "\n".join(report_lines)
        report_window = tk.Toplevel(self.parent_frame)
        report_window.title("📋 Reporte Final del Viaje")
        report_window.configure(bg="#1a1a1a")

        text_widget = tk.Text(
            report_window,
            wrap="word",
            bg="#1a1a1a",
            fg="#00ffcc",
            font=("Consolas", 11),
            height=30,
            width=70
        )
        text_widget.insert("1.0", report_text)
        text_widget.config(state="disabled")
        text_widget.pack(padx=20, pady=20)

        tk.Button(
            report_window,
            text="Cerrar",
            command=report_window.destroy,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(pady=(0, 15))
