"""
Funciones auxiliares para trabajar con estrellas (Star objects)
Facilita el acceso a objetos Star desde el star_map
"""

from typing import Dict, Optional, Any
from src.models.star import Star

def get_star_object(star_map: Dict[int, dict], star_id: int) -> Optional[Star]:
    """
    Obtiene el objeto Star dado su ID desde el star_map.
    
    Args:
        star_map: Diccionario con información de estrellas {star_id: {props...}}
        star_id: ID de la estrella a buscar
        
    Returns:
        Objeto Star si existe, None si no se encuentra
    """
    star_info = star_map.get(star_id)
    if star_info is None:
        return None
    
    return star_info.get("star_object")

def get_star_property(star_map: Dict[int, dict], star_id: int, property_name: str) -> Any:
    """
    Obtiene una propiedad específica de una estrella.
    
    Args:
        star_map: Diccionario con información de estrellas
        star_id: ID de la estrella
        property_name: Nombre de la propiedad (ej: "time_to_eat_kg", "is_hypergiant")
        
    Returns:
        Valor de la propiedad, o None si no existe
    """
    star = get_star_object(star_map, star_id)
    if star is None:
        return None
    
    return getattr(star, property_name, None)

def is_hypergiant(star_map: Dict[int, dict], star_id: int) -> bool:
    """
    Verifica si una estrella es hipergigante (portal).
    
    Args:
        star_map: Diccionario con información de estrellas
        star_id: ID de la estrella
        
    Returns:
        True si es hipergigante, False en caso contrario
    """
    star = get_star_object(star_map, star_id)
    if star is None:
        return False
    
    return star.is_hypergiant

def get_star_neighbors(star_map: Dict[int, dict], star_id: int) -> list:
    """
    Obtiene la lista de vecinos (linkedTo) de una estrella.
    
    Args:
        star_map: Diccionario con información de estrellas
        star_id: ID de la estrella
        
    Returns:
        Lista de diccionarios: [{"starId": int, "distance": float}, ...]
        Lista vacía si la estrella no existe o no tiene vecinos
    """
    star_info = star_map.get(star_id)
    if star_info is None:
        return []
    
    return star_info.get("linkedTo", [])

def update_star_property(star_map: Dict[int, dict], star_id: int, property_name: str, value: Any) -> bool:
    """
    Actualiza una propiedad de una estrella (útil para Requisito 3.a).
    
    Args:
        star_map: Diccionario con información de estrellas
        star_id: ID de la estrella
        property_name: Nombre de la propiedad a actualizar
        value: Nuevo valor
        
    Returns:
        True si se actualizó correctamente, False si la estrella no existe
    """
    star = get_star_object(star_map, star_id)
    if star is None:
        return False
    
    try:
        setattr(star, property_name, value)
        return True
    except AttributeError:
        return False
    
def get_star_info_summary(star_map: Dict[int, dict], star_id: int) -> Optional[dict]:
    """
    Obtiene un resumen completo de información de una estrella.
    
    Args:
        star_map: Diccionario con información de estrellas
        star_id: ID de la estrella
        
    Returns:
        Diccionario con toda la información relevante, None si no existe
    """
    star = get_star_object(star_map, star_id)
    if star is None:
        return None
    
    star_info = star_map.get(star_id, {})
    
    return {
        "id": star.star_id,
        "name": star.name,
        "x": star.x,
        "y": star.y,
        "time_to_eat_kg": star.time_to_eat_kg,
        "energy_cost_research": star.energy_cost_research,
        "health_impact": star.health_impact,
        "lifespan_change": star.lifespan_change,
        "is_hypergiant": star.is_hypergiant,
        "max_stay_time": star.max_stay_time,
        "constellations": star_info.get("constellations", []),
        "neighbors": star_info.get("linkedTo", [])
    }