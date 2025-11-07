"""
Algoritmo de Dijkstra Modificado para Máxima Exploración
Requisito 2: Encontrar la ruta que visite la mayor cantidad de estrellas
antes de que el burro muera.
"""

import heapq
from typing import Dict, List, Tuple, Any


def dijkstra_max_exploration(star_graph, donkey, start_star_id: int) -> Dict[str, Any]:
    """
    Algoritmo de Dijkstra modificado para maximizar estrellas visitadas.
    
    En lugar de minimizar distancia, maximizamos cantidad de estrellas visitadas
    respetando la restricción: edad_actual < edad_muerte
    
    Args:
        star_graph: Instancia de StarGraph con el grafo y datos de estrellas
        donkey: Instancia de Donkey con edad inicial y edad de muerte
        start_star_id: ID de la estrella inicial
    
    Returns:
        Diccionario con:
        - success: bool, si se encontró una ruta válida
        - route: List[int], lista de IDs de estrellas en orden
        - total_distance: float, distancia total recorrida
        - stars_visited: int, cantidad de estrellas visitadas
        - final_age: float, edad final del burro
        - remaining_life: float, vida restante (death_age - final_age)
        - message: str, mensaje descriptivo
    """
    
    # Verificar que la estrella inicial existe
    if start_star_id not in star_graph.get_all_vertices():
        return {
            "success": False,
            "route": [],
            "total_distance": 0,
            "stars_visited": 0,
            "final_age": donkey.start_age,
            "remaining_life": 0,
            "message": f"Estrella inicial {start_star_id} no existe en el grafo"
        }
    
    # Cola de prioridad: (-num_visited, current_age, current_star, path, distance)
    # Usamos -num_visited para simular max-heap (Python tiene min-heap)
    priority_queue = [(-1, donkey.start_age, start_star_id, [start_star_id], 0)]
    
    # Mejor resultado encontrado
    best_result = {
        "stars_visited": 1,
        "route": [start_star_id],
        "total_distance": 0,
        "final_age": donkey.start_age
    }
    
    # Set de estados visitados: (star_id, num_visited)
    # Permite visitar la misma estrella con diferente número de estrellas visitadas
    visited_states = set()
    
    while priority_queue:
        neg_num_visited, current_age, current_star, path, total_distance = heapq.heappop(priority_queue)
        num_visited = -neg_num_visited
        
        # Crear estado único
        state = (current_star, num_visited)
        if state in visited_states:
            continue
        visited_states.add(state)
        
        # Actualizar mejor resultado si encontramos más estrellas
        if num_visited > best_result["stars_visited"]:
            best_result = {
                "stars_visited": num_visited,
                "route": path.copy(),
                "total_distance": total_distance,
                "final_age": current_age
            }
        
        # Explorar vecinos
        neighbors = star_graph.get_neighbors_with_distance(current_star)
        
        for neighbor_id, distance in neighbors:
            # Calcular nueva edad
            new_age = current_age + distance
            
            # Restricción: NO debe llegar a la edad de muerte
            if new_age >= donkey.death_age:
                continue
            
            # Evitar ciclos en el path actual
            if neighbor_id in path:
                continue
            
            # Crear nuevo path
            new_path = path + [neighbor_id]
            new_num_visited = num_visited + 1
            new_total_distance = total_distance + distance
            
            # Agregar a la cola con prioridad negativa (para max-heap)
            heapq.heappush(
                priority_queue,
                (-new_num_visited, new_age, neighbor_id, new_path, new_total_distance)
            )
    
    # Calcular vida restante
    remaining_life = donkey.death_age - best_result["final_age"]
    
    return {
        "success": True,
        "route": best_result["route"],
        "total_distance": best_result["total_distance"],
        "stars_visited": best_result["stars_visited"],
        "final_age": best_result["final_age"],
        "remaining_life": remaining_life,
        "message": f"Ruta encontrada: {best_result['stars_visited']} estrellas visitadas"
    }


def format_route_info(result: Dict[str, Any]) -> str:
    """
    Formatea el resultado del algoritmo en un string legible.
    
    Args:
        result: Diccionario retornado por dijkstra_max_exploration
    
    Returns:
        String formateado con la información de la ruta
    """
    if not result["success"]:
        return f"❌ {result['message']}"
    
    route_str = " → ".join(map(str, result["route"]))
    
    return (
        f"✅ RUTA DE MÁXIMA EXPLORACIÓN\n"
        f"{'='*50}\n"
        f"🌟 Estrellas visitadas: {result['stars_visited']}\n"
        f"📍 Ruta: {route_str}\n"
        f"📏 Distancia total: {result['total_distance']:.2f} años luz\n"
        f"🎂 Edad final: {result['final_age']:.2f} años luz\n"
        f"💚 Vida restante: {result['remaining_life']:.2f} años luz\n"
        f"{'='*50}"
    )
