"""
StarGraph - Grafo integrado con información de estrellas
Combina graphBase con star_map para facilitar algoritmos
"""

from typing import Dict, List, Optional, Tuple
from src.models.graphBase import graphBase
from src.utils.star_helpers import (
    get_star_object,
    get_star_property,
    get_star_neighbors,
    is_hypergiant
)

class StarGraph:
    """
    Grafo que integra información de estrellas con conexiones.
    Facilita el acceso a propiedades de estrellas durante algoritmos.
    """
    
    def __init__(self, graph: graphBase, star_map: Dict[int, dict]):
        """
        Inicializa el StarGraph.
        
        Args:
            graph: Objeto graphBase con las conexiones entre estrellas
            star_map: Diccionario con información completa de estrellas
        """
        self.graph = graph
        self.star_map = star_map

    def get_all_vertices(self) -> List[int]:
        """
        Obtiene lista de todos los IDs de estrellas en el grafo.
        
        Returns:
            Lista de IDs de estrellas
        """
        return self.graph.get_vertices()
    
    def get_neighbors_with_distance(self, star_id: int) -> Dict[int, float]:
        """
        Obtiene los vecinos de una estrella con sus distancias.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            Diccionario {neighbor_id: distance}
            
        Example:
            neighbors = star_graph.get_neighbors_with_distance(1)
            # {2: 120, 4: 87, 5: 101}
        """
        return self.graph.get_neighbors(star_id)
    
    def get_star(self, star_id: int):
        """
        Obtiene el objeto Star completo.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            Objeto Star o None si no existe
        """
        return get_star_object(self.star_map, star_id)
    
    def get_star_property(self, star_id: int, property_name: str):
        """
        Obtiene una propiedad específica de una estrella.
        
        Args:
            star_id: ID de la estrella
            property_name: Nombre de la propiedad
            
        Returns:
            Valor de la propiedad o None
            
        Example:
            time = star_graph.get_star_property(1, "time_to_eat_kg")
        """
        return get_star_property(self.star_map, star_id, property_name)
    
    def is_hypergiant_star(self, star_id: int) -> bool:
        """
        Verifica si una estrella es hipergigante (portal).
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            True si es hipergigante, False en caso contrario
        """
        return is_hypergiant(self.star_map, star_id)
    
    def get_distance_between(self, star_id_a: int, star_id_b: int) -> Optional[float]:
        """
        Obtiene la distancia directa entre dos estrellas vecinas.
        
        Args:
            star_id_a: ID de la primera estrella
            star_id_b: ID de la segunda estrella
            
        Returns:
            Distancia en años luz, o None si no son vecinas
            
        Example:
            distance = star_graph.get_distance_between(1, 2)
            # 120
        """
        neighbors = self.graph.get_neighbors(star_id_a)
        return neighbors.get(star_id_b, None)
    
    def get_star_info(self, star_id: int) -> Optional[dict]:
        """
        Obtiene toda la información relevante de una estrella.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            Diccionario con información completa de la estrella
        """
        star = self.get_star(star_id)
        if star is None:
            return None
        
        neighbors = self.get_neighbors_with_distance(star_id)
        
        return {
            "id": star.star_id,
            "name": star.name,
            "position": (star.x, star.y),
            "time_to_eat_kg": star.time_to_eat_kg,
            "energy_cost_research": star.energy_cost_research,
            "health_impact": star.health_impact,
            "lifespan_change": star.lifespan_change,
            "is_hypergiant": star.is_hypergiant,
            "max_stay_time": star.max_stay_time,
            "neighbors": neighbors
        }
    
    def count_stars(self) -> int:
        """
        Cuenta el número total de estrellas en el grafo.
        
        Returns:
            Número de estrellas
        """
        return len(self.star_map)
    
    def __repr__(self):
        """Representación en string del StarGraph"""
        return f"StarGraph(stars={self.count_stars()}, vertices={len(self.get_all_vertices())})"