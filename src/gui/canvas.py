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
    
    def draw_route(self, route: list, color="#00ff00", width=4):
        """
        Dibuja una ruta sobre el mapa existente con mejoras visuales.
        
        Args:
            route: Lista de IDs de estrellas en orden [1, 3, 5, ...]
            color: Color de la ruta (por defecto verde brillante)
            width: Grosor de la línea
        """
        if not route or len(route) < 2:
            return
        
        # Eliminar rutas anteriores (si existen)
        self.delete("route")
        
        # Dibujar líneas conectando las estrellas de la ruta
        for i in range(len(route) - 1):
            star_id_from = route[i]
            star_id_to = route[i + 1]
            
            # Obtener coordenadas de las estrellas
            if star_id_from not in self.star_map or star_id_to not in self.star_map:
                continue
            
            star_from = self.star_map[star_id_from]
            star_to = self.star_map[star_id_to]
            
            # Escalar coordenadas
            x1, y1 = self._scale_coords(star_from["coordenates"]["x"], star_from["coordenates"]["y"])
            x2, y2 = self._scale_coords(star_to["coordenates"]["x"], star_to["coordenates"]["y"])
            
            # Dibujar sombra (línea más gruesa oscura detrás)
            self.create_line(
                x1, y1, x2, y2,
                fill="#003300",  # Verde oscuro para sombra
                width=width + 2,
                tags="route"
            )
            
            # Dibujar línea principal
            self.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width,
                arrow="last",  # Flecha al final
                arrowshape=(16, 20, 6),  # Flecha más grande
                tags="route"
            )
        
        # Resaltar estrellas de la ruta con números y nombres
        for i, star_id in enumerate(route):
            if star_id not in self.star_map:
                continue
            
            star = self.star_map[star_id]
            x, y = self._scale_coords(star["coordenates"]["x"], star["coordenates"]["y"])
            
            # Color especial para la primera y última estrella
            if i == 0:
                circle_color = "#00ff00"  # Verde brillante (inicio)
                text_color = "#00ff00"
            elif i == len(route) - 1:
                circle_color = "#ff0000"  # Rojo (fin)
                text_color = "#ff0000"
            else:
                circle_color = "#ffff00"  # Amarillo (intermedio)
                text_color = "#ffff00"
            
            # Dibujar círculo resaltado
            radius = 18
            self.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                outline=circle_color,
                width=4,
                tags="route"
            )
            
            # Dibujar número de orden (más grande)
            self.create_text(
                x, y - 30,
                text=str(i + 1),
                fill=text_color,
                font=("Arial", 16, "bold"),
                tags="route"
            )
            
            # Dibujar nombre de la estrella debajo
            star_name = star.get("label", f"Star {star_id}")
            self.create_text(
                x, y + 30,
                text=star_name,
                fill="#ffffff",
                font=("Arial", 10, "bold"),
                tags="route"
            )
    
    def clear_route(self):
        """Elimina la ruta dibujada del canvas"""
        self.delete("route")

    def draw_donkey(self, star_id:int):
        """
        Dibuja el ícono del burro en la estrella dada.
        Args:
            star_id: ID de la estrella donde dibujar el burro
        """
        #Eliminar el burro anterior
        self.delete("donkey")

        if star_id not in self.star_map:
            return

        star = self.star_map[star_id]
        x, y = self._scale_coords(star["coordenates"]["x"], star["coordenates"]["y"])

        #Por ahora dibuja un burro simple
        radius = 25
        self.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="#8B4513",  # Marrón
            outline="#5D2E0F",
            width=3,
            tags="donkey"
        )
        
        # Emoji del burro
        self.create_text(
            x, y,
            text="🐴",
            font=("Arial", 30),
            tags="donkey"
        )
        
        # Etiqueta "BURRO AQUÍ"
        self.create_text(
            x, y - 45,
            text="🐴 BURRO AQUÍ",
            fill="#ffffff",
            font=("Arial", 10, "bold"),
            tags="donkey"
        )
    
    def clear_donkey(self):
        """Elimina el ícono del burro del canvas"""
        self.delete("donkey")