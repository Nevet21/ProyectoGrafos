# star_renderer.py
import tkinter as tk
from typing import Dict, List, Callable, Tuple

class StarRenderer:
    """
    Clase responsable de dibujar estrellas, conexiones y leyendas en el canvas.
    Separa la lógica de renderizado de la lógica del canvas.
    """
    
    def __init__(self, canvas: tk.Canvas, star_map: Dict[int, dict], 
                constellations: List[dict], scale_func: Callable,
                constellation_colors: List[str]):
        """
        Inicializa el renderizador con los datos necesarios.
        
        Args:
            canvas: Canvas de tkinter donde se dibujará
            star_map: Diccionario con información de estrellas
            constellations: Lista de constelaciones
            scale_func: Función que convierte coords JSON a coords canvas
            constellation_colors: Lista de colores para constelaciones
        """
        self.canvas = canvas
        self.star_map = star_map
        self.constellations = constellations
        self.scale_coords = scale_func  # Guardamos la función
        self.constellation_colors = constellation_colors
        
        # Crear mapa de constelación -> color
        self.constellation_color_map = {}
        for i, const in enumerate(self.constellations):
            color_index = i % len(self.constellation_colors)
            self.constellation_color_map[const["name"]] = self.constellation_colors[color_index]

    def draw_all(self):
        """
        Dibuja todos los elementos: conexiones, estrellas y leyenda.
        Orden importante: líneas primero, luego estrellas encima.
        """
        # 1. Dibujar conexiones (líneas) primero
        self.draw_connections()
        
        # 2. Dibujar estrellas encima de las líneas
        self.draw_stars()
        
        # 3. Dibujar leyenda al final (encima de todo)
        self.draw_legend()

    def draw_connections(self):
        """
        Dibuja las líneas que conectan las estrellas según linkedTo.
        Evita duplicados (no dibujar la misma línea dos veces).
        """
        drawn_connections = set()  # Para rastrear conexiones ya dibujadas
        
        for star_id, star in self.star_map.items():
            # Obtener coordenadas escaladas de la estrella origen
            x1, y1 = self.scale_coords(
                star["coordenates"]["x"],
                star["coordenates"]["y"]
            )
            
            # Dibujar línea a cada vecino
            for neighbor in star.get("linkedTo", []):
                neighbor_id = neighbor.get("starId")
                
                # Verificar que el vecino existe en el mapa
                if neighbor_id not in self.star_map:
                    continue
                
                # Crear identificador único de la conexión (ordenado)
                # Ejemplo: conexión entre 1 y 2 siempre será (1, 2)
                connection = tuple(sorted([star_id, neighbor_id]))
                
                # Si ya dibujamos esta conexión, saltarla
                if connection in drawn_connections:
                    continue
                
                # Marcar como dibujada
                drawn_connections.add(connection)
                
                # Obtener coordenadas del vecino
                neighbor_star = self.star_map[neighbor_id]
                x2, y2 = self.scale_coords(
                    neighbor_star["coordenates"]["x"],
                    neighbor_star["coordenates"]["y"]
                )
                
                # Obtener la distancia (opcional, para mostrarla)
                distance = neighbor.get("distance", "?")
                
                # Dibujar la línea
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill="#34495e",  # Gris oscuro
                    width=1,
                    tags="connection"
                )
                
                # Dibujar etiqueta con la distancia en el punto medio de la línea
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Fondo semitransparente para la etiqueta (rectángulo oscuro)
                distance_text = f"{distance:.1f}" if isinstance(distance, (int, float)) else str(distance)
                
                # Crear texto con fondo para mejor visibilidad
                self.canvas.create_text(
                    mid_x, mid_y,
                    text=distance_text,
                    fill="#3498db",  # Azul claro
                    font=("Arial", 8, "bold"),
                    tags="connection"
                )

    def draw_stars(self):
        """
        Dibuja cada estrella como un círculo.
        - Color según constelación
        - ROJO si es compartida
        - Borde grueso si es hipergigante
        """
        for star_id, star in self.star_map.items():
            # Obtener coordenadas escaladas
            cx, cy = self.scale_coords(
                star["coordenates"]["x"],
                star["coordenates"]["y"]
            )
            
            # Determinar el color de la estrella
            color = self._get_star_color(star)
            
            # Calcular tamaño del círculo
            radius_px = self._get_star_radius(star)
            
            # Determinar grosor del borde (hipergigantes tienen borde grueso)
            border_width = 3 if star.get("hypergiant", False) else 1
            
            # Dibujar el círculo de la estrella
            self.canvas.create_oval(
                cx - radius_px, cy - radius_px,  # Esquina superior izquierda
                cx + radius_px, cy + radius_px,  # Esquina inferior derecha
                fill=color,
                outline="white",
                width=border_width,
                tags=f"star_{star_id}"
            )
            
            # Dibujar etiqueta encima de la estrella
            self._draw_star_label(star, cx, cy, radius_px)

    def _get_star_color(self, star: dict) -> str:
        """
        Determina el color de una estrella.
        
        Returns:
            Color hexadecimal (#RRGGBB)
        """
        # Si es compartida, siempre ROJO
        if star.get("shared_by_coords", False):
            return "#e74c3c"  # Rojo
        
        # Si no, usar color de su primera constelación
        const_name = star["constellations"][0]
        return self.constellation_color_map.get(const_name, "white")
    
    def _get_star_radius(self, star: dict) -> float:
        """
        Calcula el radio en píxeles para dibujar la estrella.
        
        Returns:
            Radio en píxeles
        """
        # Obtener radio del JSON (default 0.5)
        json_radius = star.get("radius", 0.5)
        
        # Escalar para que sea visible (multiplicar por 10-15)
        base_radius = json_radius * 12
        
        # Mínimo 5 píxeles para que sea visible
        return max(base_radius, 5)
    
    def _draw_star_label(self, star: dict, cx: float, cy: float, radius: float):
        """
        Dibuja la etiqueta (label) de la estrella encima de ella.
        
        Args:
            star: Diccionario con datos de la estrella
            cx, cy: Coordenadas del centro en canvas
            radius: Radio de la estrella en píxeles
        """
        label_text = star.get("label", str(star["id"]))
        
        # Posicionar encima de la estrella
        label_y = cy - radius - 10
        
        self.canvas.create_text(
            cx, label_y,
            text=label_text,
            fill="white",
            font=("Arial", 8, "bold"),
            tags=f"label_{star['id']}"
        )

    def draw_legend(self):
        """
        Dibuja una leyenda en la esquina superior izquierda
        explicando los colores de las constelaciones.
        """
        legend_x = 10
        legend_y = 10
        line_height = 20
        
        # Título de la leyenda
        self.canvas.create_text(
            legend_x, legend_y,
            text="Leyenda:",
            fill="white",
            font=("Arial", 10, "bold"),
            anchor="nw"  # Anclar en esquina noroeste (arriba-izquierda)
        )
        
        # Dibujar cada constelación
        y_offset = 25
        for const in self.constellations:
            color = self.constellation_color_map[const["name"]]
            
            # Círculo de muestra
            self.canvas.create_oval(
                legend_x, legend_y + y_offset,
                legend_x + 15, legend_y + y_offset + 15,
                fill=color,
                outline="white"
            )
            
            # Nombre de la constelación
            self.canvas.create_text(
                legend_x + 20, legend_y + y_offset + 7,
                text=const["name"],
                fill="white",
                font=("Arial", 9),
                anchor="w"  # Anclar a la izquierda (west)
            )
            
            y_offset += line_height
        
        # Indicador de estrella compartida
        self.canvas.create_oval(
            legend_x, legend_y + y_offset,
            legend_x + 15, legend_y + y_offset + 15,
            fill="#e74c3c",  # Rojo
            outline="white"
        )
        self.canvas.create_text(
            legend_x + 20, legend_y + y_offset + 7,
            text="Estrella compartida",
            fill="white",
            font=("Arial", 9),
            anchor="w"
        )