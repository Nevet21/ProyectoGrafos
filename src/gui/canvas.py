import tkinter as tk
from typing import Dict, List, Tuple
from .star_renderer import StarRenderer

class StarMapCanvas(tk.Canvas):
    """
    Canvas personalizado para dibujar el mapa de estrellas y constelaciones.
    Hereda de tk.Canvas para tener todas las funcionalidades de dibujo.
    """
    def __init__(self, parent, width=800, height=800, **kwargs):
        super().__init__(parent, width=width, height=height, bg="black", **kwargs)

        # Dimensiones del canvas
        self.canvas_width = width
        self.canvas_height = height

        # Datos del mapa de estrellas, aún no asignados
        self.star_map = {}
        self.constellations = []

        # Colores para cada constelación
        self.constellation_colors = [
            "#3498db",  # Azul
            "#2ecc71",  # Verde
            "#e74c3c",  # Rojo
            "#f39c12",  # Naranja
            "#9b59b6",  # Púrpura
            "#1abc9c",  # Turquesa
            "#34495e",  # Gris oscuro
        ]

        # Escalado (Esto nos ayuda a ajustar dimensiones desde el JSON al Canvas)
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 50  # Margen izquierdo
        self.offset_y = 50  # Margen superior

    def load_data(self, star_map: Dict[int, dict], constellations: List[dict]):
        """
        Carga los datos del mapa de estrellas y constelaciones.
        Necesitamos Args:
            - Star_map: Diccionario {star_id: {propiedades...}}
            constellations: Lista de constelaciones con sus estrellas
        """
        self.star_map = star_map
        self.constellations = constellations

        #Calcular el escalado basado en las coordenadas
        self._calculate_scaling()

    def _calculate_scaling(self):
        """
        Calcula los factores de escalado para ajustar las coordenadas del JSON
        al tamaño del Canvas.
        """
        if not self.star_map:
            return
        
        #Para encontrar coordenadas mínimas y máximas
        min_x = min(star["coordenates"]["x"] for star in self.star_map.values())
        max_x = max(star["coordenates"]["x"] for star in self.star_map.values())
        min_y = min(star["coordenates"]["y"] for star in self.star_map.values())
        max_y = max(star["coordenates"]["y"] for star in self.star_map.values())

        #Calcular el rango de coordenadas
        range_x = max_x - min_x
        range_y = max_y - min_y

        # Editar división por cero
        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1

        # Calcular el área útil del canvas (restando márgenes)
        usable_width = self.canvas_width - (2 * self.offset_x)
        usable_height = self.canvas_height - (2 * self.offset_y)

        #Calcular el factor de escala (el más pequeño para que todo quepa)
        self.scale_x = usable_width / range_x
        self.scale_y = usable_height / range_y

        #Usar la misma escala para los dos ejes X y Y
        self.scale = min(self.scale_x, self.scale_y)

        #Guardar los mínimos para trasladar el origen
        self.min_x = min_x
        self.min_y = min_y

    def _scale_coords(self, x: float, y: float) -> Tuple[float, float]:
            """
            Convierte las coordenadas del JSON a coordenadas del Canvas.

            Args:
            x, y coordenadas originales del JSON

            Returns:
                Una tupla con (canvas_x, canvas_y) ya escaladas
            """

            #Trasladar al origen (restar mínimos)
            x_translated = x - self.min_x
            y_translated = y - self.min_y

            #Escalar
            canvas_x = (x_translated * self.scale) + self.offset_x
            canvas_y = (y_translated * self.scale) + self.offset_y

            return canvas_x, canvas_y
        
    def draw_map(self):
        """
        Dibuja todo el mapa estelar: conexiones y estrellas
        Deja las tareas a StarRenderer
        """

        #Limpiar el canvas antes de dibujar
        self.delete("all")

        if not self.star_map:
            #Si no hay datos, mostrar mensaje
            self.create_text(
                self.canvas_width / 2,
                self.canvas_height / 2,
                text="No hay datos cargados\nHaz Click en 'Cargar JSON",
                fill="white",
                font=("Arial", 16),
                justify="center"
            )
            return
    
        # Crear el renderizador y dibujar
        renderer = StarRenderer(
            canvas=self,
            star_map=self.star_map,
            constellations=self.constellations,
            scale_func=self._scale_coords,
            constellation_colors=self.constellation_colors
        )
         
        renderer.draw_all()