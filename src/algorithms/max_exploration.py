"""
Algoritmos para calcular la ruta de máxima exploración (Requisito 2)
Usa Dijkstra modificado para encontrar la ruta que visita más estrellas
"""

import heapq
from typing import List, Tuple, Dict, Set, Optional
from src.models.star_graph import StarGraph
from src.models.donkey import Donkey

def dijkstra_max_exploration(star_graph: StarGraph, donkey: Donkey, start_star_id: int) -> Dict:
    """
    Algoritmo de Dijkstra modificado para encontrar la ruta que visita 
    la MAYOR cantidad de estrellas antes de que el burro muera.
    
    Diferencias con Dijkstra clásico:
    - En lugar de minimizar distancia, MAXIMIZAMOS número de nodos visitados
    - Restricción: edad_actual + distancia <= edad_muerte
    - Prioridad: -num_visitadas (negativo para que heapq sea max-heap)
    
    Args:
        star_graph: Grafo con estrellas
        donkey: Burro con edad inicial y edad de muerte
        start_star_id: ID de la estrella de inicio
        
    Returns:
        Dict con:
            - route: Lista de IDs de estrellas en orden de visita
            - total_distance: Distancia total recorrida
            - stars_visited: Número de estrellas visitadas
            - final_age: Edad final del burro
            - success: True si encontró una ruta, False si no
    """
    
    # Verificar que la estrella inicial existe
    if star_graph.get_star(start_star_id) is None:
        return {
            "route": [],
            "total_distance": 0,
            "stars_visited": 0,
            "final_age": donkey.current_age,
            "success": False,
            "message": f"Estrella inicial {start_star_id} no existe"
        }
    
    # Cola de prioridad: (prioridad, edad_actual, estrella_actual, ruta, visitados)
    # Prioridad = -len(visitados) para que sea max-heap (más estrellas = mayor prioridad)
    initial_state = (
        -1,                      # Prioridad: -1 porque ya visitamos 1 estrella
        donkey.current_age,      # Edad actual
        start_star_id,           # Estrella actual
        [start_star_id],         # Ruta hasta ahora
        {start_star_id}          # Set de visitados (para búsqueda O(1))
    )
    
    heap = [initial_state]
    
    # Mejor solución encontrada hasta ahora
    best_solution = {
        "route": [start_star_id],
        "total_distance": 0,
        "stars_visited": 1,
        "final_age": donkey.current_age,
        "success": True
    }
    
    # Dijkstra modificado
    iterations = 0
    max_iterations = 10000  # Límite de seguridad
    
    while heap and iterations < max_iterations:
        iterations += 1
        
        # Extraer el estado con más estrellas visitadas
        neg_count, current_age, current_star, route, visited = heapq.heappop(heap)
        num_visited = -neg_count
        
        # Calcular distancia total de la ruta actual
        total_distance = 0
        for i in range(len(route) - 1):
            dist = star_graph.get_distance_between(route[i], route[i + 1])
            if dist:
                total_distance += dist
        
        # Si esta ruta es mejor que la mejor encontrada, actualizarla
        if num_visited > best_solution["stars_visited"]:
            best_solution = {
                "route": route.copy(),
                "total_distance": total_distance,
                "stars_visited": num_visited,
                "final_age": current_age,
                "success": True
            }
        
        # Explorar vecinos
        neighbors = star_graph.get_neighbors_with_distance(current_star)
        
        for neighbor_id, distance in neighbors.items():
            # Si ya visitamos esta estrella, saltar
            if neighbor_id in visited:
                continue
            
            # Calcular nueva edad después de viajar
            new_age = current_age + distance
            
            # Verificar si el burro sobreviviría el viaje
            if new_age >= donkey.death_age:
                continue  # No puede hacer este viaje, moriría
            
            # Crear nuevo estado
            new_route = route + [neighbor_id]
            new_visited = visited | {neighbor_id}  # Union de sets
            new_state = (
                -len(new_visited),   # Prioridad: más estrellas = mejor
                new_age,
                neighbor_id,
                new_route,
                new_visited
            )
            
            # Agregar a la cola de prioridad
            heapq.heappush(heap, new_state)
    
    # Agregar información adicional
    best_solution["iterations"] = iterations
    best_solution["remaining_life"] = donkey.death_age - best_solution["final_age"]
    
    return best_solution

def format_route_info(result: Dict, star_graph: StarGraph) -> str:
    """
    Formatea la información de una ruta para mostrarla de forma legible.
    
    Args:
        result: Diccionario con resultado de dijkstra_max_exploration
        star_graph: Grafo para obtener nombres de estrellas
        
    Returns:
        String formateado con información de la ruta
    """
    if not result["success"]:
        return f"❌ Error: {result.get('message', 'No se pudo calcular la ruta')}"
    
    output = []
    output.append("=" * 70)
    output.append("📍 RUTA DE MÁXIMA EXPLORACIÓN (Requisito 2)")
    output.append("=" * 70)
    output.append(f"✓ Estrellas visitadas: {result['stars_visited']}")
    output.append(f"✓ Distancia total: {result['total_distance']:.2f} años luz")
    output.append(f"✓ Edad final: {result['final_age']:.2f} años luz")
    output.append(f"✓ Vida restante: {result['remaining_life']:.2f} años luz")
    output.append(f"✓ Iteraciones: {result['iterations']}")
    output.append("")
    output.append("🗺️ RUTA DETALLADA:")
    
    route = result["route"]
    for i, star_id in enumerate(route):
        star = star_graph.get_star(star_id)
        if star:
            output.append(f"   {i + 1}. Estrella {star_id}: {star.name}")
        else:
            output.append(f"   {i + 1}. Estrella {star_id}")
        
        # Mostrar distancia al siguiente
        if i < len(route) - 1:
            next_star_id = route[i + 1]
            distance = star_graph.get_distance_between(star_id, next_star_id)
            output.append(f"       ↓ {distance} años luz")
    
    output.append("=" * 70)
    
    return "\n".join(output)