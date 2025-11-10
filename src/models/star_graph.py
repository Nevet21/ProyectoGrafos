"""
StarGraph: Wrapper que combina graphBase con star_map para operaciones convenientes
"""

from typing import Dict, List, Tuple, Optional, Any
from .graphBase import graphBase


class StarGraph:
    """
    Wrapper que combina un grafo (graphBase) con un star_map para facilitar
    operaciones relacionadas con estrellas.
    """

    def __init__(self, graph: graphBase, star_map: Dict[int, Dict[str, Any]]):
        """
        Inicializa el StarGraph.

        Args:
            graph: Instancia de graphBase con las relaciones entre estrellas
            star_map: Diccionario con información de todas las estrellas {id: star_data}
        """
        self.graph = graph
        self.star_map = star_map

    def get_all_vertices(self) -> List[int]:
        """
        Obtiene todos los vértices (IDs de estrellas) del grafo.

        Returns:
            Lista con todos los IDs de estrellas
        """
        return self.graph.get_vertices()

    def get_neighbors_with_distance(self, star_id: int) -> List[Tuple[int, float]]:
        """
        Obtiene los vecinos de una estrella con sus distancias, ignorando caminos bloqueados.
        """
        neighbors_dict = self.graph.get_neighbors(star_id)

        result = []
        for neighbor_id, edge_data in neighbors_dict.items():
            # Si el grafo guarda solo la distancia (float), conviértelo en dict
            if isinstance(edge_data, dict):
                if not edge_data.get("blocked", False):
                    result.append((neighbor_id, edge_data.get("distance", 0)))
            else:
                # Si solo hay distancia numérica, asumimos que no está bloqueado
                result.append((neighbor_id, edge_data))
        return result


    def get_star(self, star_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene la información completa de una estrella.

        Args:
            star_id: ID de la estrella

        Returns:
            Diccionario con la información de la estrella o None si no existe
        """
        return self.star_map.get(star_id)

    def get_star_property(self, star_id: int, property_name: str) -> Any:
        """
        Obtiene una propiedad específica de una estrella.

        Args:
            star_id: ID de la estrella
            property_name: Nombre de la propiedad (ej: "name", "hypergiant", "coordenates")

        Returns:
            Valor de la propiedad o None si no existe
        """
        star = self.get_star(star_id)
        if star is None:
            return None
        return star.get(property_name)

    def is_hypergiant_star(self, star_id: int) -> bool:
        """
        Verifica si una estrella es hipergigante.

        Args:
            star_id: ID de la estrella

        Returns:
            True si es hipergigante, False en caso contrario
        """
        return self.get_star_property(star_id, "hypergiant") or False

    def get_distance_between(self, star_id1: int, star_id2: int) -> Optional[float]:
        """
        Obtiene la distancia entre dos estrellas si están conectadas.

        Args:
            star_id1: ID de la primera estrella
            star_id2: ID de la segunda estrella

        Returns:
            Distancia entre las estrellas o None si no están conectadas
        """
        neighbors = self.graph.get_neighbors(star_id1)
        return neighbors.get(star_id2)

    def get_star_info(self, star_id: int) -> str:
        """
        Genera un resumen legible de la información de una estrella.

        Args:
            star_id: ID de la estrella

        Returns:
            String con información resumida de la estrella
        """
        star = self.get_star(star_id)
        if star is None:
            return f"Estrella {star_id} no encontrada"

        name = star.get("name", "Sin nombre")
        hypergiant = " 💫 (HIPERGIGANTE)" if star.get("hypergiant") else ""
        coords = star.get("coordenates", {})
        x, y = coords.get("x", 0), coords.get("y", 0)

        neighbors = self.get_neighbors_with_distance(star_id)
        neighbor_count = len(neighbors)

        return (
            f"⭐ {name} (ID: {star_id}){hypergiant}\n"
            f"   Coordenadas: ({x}, {y})\n"
            f"   Conexiones: {neighbor_count} estrellas"
        )

    def count_stars(self) -> int:
        """
        Cuenta el número total de estrellas en el grafo.

        Returns:
            Número de estrellas
        """
        return len(self.star_map)
    
        # ==========================================================
    # 🛰️ NUEVOS MÉTODOS PARA BLOQUEAR Y HABILITAR CAMINOS (Requisito 4)
    # ==========================================================

    def _init_blocked_edges(self):
        """Inicializa la estructura de caminos bloqueados (si aún no existe)."""
        if not hasattr(self, "blocked_edges"):
            self.blocked_edges = set()

    def set_edge_blocked(self, star_id1: int, star_id2: int, blocked: bool = True):
        """
        Bloquea o habilita un camino entre dos estrellas (en ambos sentidos).
        """
        self._init_blocked_edges()
        edge = tuple(sorted((star_id1, star_id2)))
        if blocked:
            self.blocked_edges.add(edge)
        else:
            self.blocked_edges.discard(edge)

    def is_edge_blocked(self, star_id1: int, star_id2: int) -> bool:
        """
        Verifica si una conexión entre dos estrellas está bloqueada.
        """
        self._init_blocked_edges()
        return tuple(sorted((star_id1, star_id2))) in self.blocked_edges

    def get_all_edges(self) -> List[Tuple[int, int, float, bool]]:
        """
        Devuelve todas las aristas con su distancia y estado de bloqueo.
        Compatible con graphBase.adjacency_list.
        """
        self._init_blocked_edges()
        edges = []
        for a in self.graph.get_vertices():
            for b, distance in self.graph.get_neighbors(a).items():
                if a < b:  # Evita duplicados (grafo no dirigido)
                    blocked = self.is_edge_blocked(a, b)
                    edges.append((a, b, distance, blocked))
        return edges

    def get_neighbors_with_distance(self, star_id: int) -> List[Tuple[int, float]]:
        """
        Obtiene los vecinos de una estrella con sus distancias,
        ignorando los caminos bloqueados.
        """
        self._init_blocked_edges()
        neighbors_dict = self.graph.get_neighbors(star_id)
        result = []
        for neighbor_id, distance in neighbors_dict.items():
            if not self.is_edge_blocked(star_id, neighbor_id):
                result.append((neighbor_id, distance))
        return result

    
    
