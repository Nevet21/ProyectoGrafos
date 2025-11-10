import tkinter as tk
from tkinter import ttk, messagebox

class PathControlPanel(tk.Frame):
    """
    Panel para habilitar o bloquear caminos entre estrellas (Requisito 4).
    Permite seleccionar un par de estrellas conectadas y cambiar su estado.
    """

    def __init__(self, parent, canvas, star_graph):
        super().__init__(parent, bg="#2c3e50", padx=10, pady=10)
        self.canvas = canvas
        self.star_graph = star_graph

        # Título
        title = tk.Label(
            self,
            text="🛰️ Control de Caminos (Requisito 4)",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack(pady=(0, 8))

        # Combobox de conexiones disponibles
        self.edge_selector = ttk.Combobox(self, width=45, state="readonly")
        self.edge_selector.pack(pady=5)

        # Botón para alternar bloqueo
        self.toggle_button = tk.Button(
            self,
            text="🔒 Bloquear / 🔓 Habilitar",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            cursor="hand2",
            command=self.toggle_edge_block
        )
        self.toggle_button.pack(pady=5)

        # Botón para refrescar lista
        refresh_button = tk.Button(
            self,
            text="🔄 Actualizar lista de caminos",
            font=("Arial", 10),
            bg="#16a085",
            fg="white",
            activebackground="#1abc9c",
            cursor="hand2",
            command=self.update_edge_list
        )
        refresh_button.pack(pady=5)

        # Estado actual del camino seleccionado
        self.status_label = tk.Label(
            self,
            text="Seleccione un camino para ver su estado.",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.status_label.pack(pady=(10, 0))

        # Cargar lista inicial de aristas
        self.update_edge_list()

    def update_edge_list(self):
        """Actualiza la lista de caminos disponibles."""
        edges = self.star_graph.get_all_edges()
        edge_labels = [f"{a} ↔ {b}  (Distancia: {dist} años luz)" for a, b, dist, _ in edges]
        self.edge_selector["values"] = edge_labels
        if edges:
            self.edge_selector.current(0)
        self.status_label.config(text="Lista actualizada. Selecciona un camino.")

    def toggle_edge_block(self):
        """Alterna el estado (bloqueado/habilitado) del camino seleccionado."""
        selection = self.edge_selector.get()
        if not selection:
            messagebox.showwarning("Aviso", "Selecciona un camino primero.")
            return

        try:
            # Extraer IDs de estrellas del texto "1 ↔ 2 (Distancia...)"
            parts = selection.split("↔")
            star_id1 = int(parts[0].strip())
            star_id2 = int(parts[1].split("(")[0].strip())
        except Exception:
            messagebox.showerror("Error", "No se pudo interpretar el camino seleccionado.")
            return

        # Verificar estado actual
        is_blocked = self.star_graph.is_edge_blocked(star_id1, star_id2)

        # Cambiar estado
        self.star_graph.set_edge_blocked(star_id1, star_id2, not is_blocked)

        # Actualizar visualización en el mapa
        self.canvas.highlight_blocked_edges(self.star_graph)

        # Mostrar mensaje de estado
        new_state = "🔒 BLOQUEADO" if not is_blocked else "🔓 HABILITADO"
        self.status_label.config(
            text=f"Camino {star_id1} ↔ {star_id2} ahora está {new_state}.",
            fg="#e74c3c" if not is_blocked else "#2ecc71"
        )
