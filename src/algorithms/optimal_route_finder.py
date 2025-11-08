"""
OptimalRouteFinder - Encuentra la ruta óptima con simulación completa (Requisito 3)
Maximiza estrellas visitadas y minimiza gasto de energía
"""

import heapq
from typing import Dict, List, Any, Optional
from .optimal_route import RouteSimulator

class OptimalRouteFinder:
    """
    Encuentra la ruta óptima que maximiza estrellas visitadas 
    y minimiza gasto de energía usando simulación completa.
    """

    def __init__(self, star_graph, star_map):
        """
        Inicializa el buscador de rutas.
        
        Args:
            star_graph: Instancia de StarGraph
        """
        self.star_graph = star_graph
        self.star_map = star_map

    def calculate_optimal_route(self, start_star_id: int, donkey, research_config: Optional[Dict] = None):
        """
        Calcula la ruta óptima desde una estrella inicial.
        
        Usa algoritmo modificado que:
        1. Maximiza cantidad de estrellas visitadas
        2. Minimiza gasto de energía
        3. Simula TODO el proceso (comer, investigar, viajar)
        
        Args:
            start_star_id: ID de la estrella inicial
            donkey: Instancia de Donkey (se clonará, no se modifica el original)
            research_config: Configuración de investigación {star_id: params}
            
        Returns:
            dict con:
            - success: bool
            - route: List[int] - IDs de estrellas en orden
            - simulation_steps: List[dict] - Info detallada de cada paso
            - final_donkey_state: dict
            - total_stars_visited: int
            - total_energy_spent: float
            - message: str
        """
        # Verificar que la estrella inicial existe
        if start_star_id not in self.star_graph.get_all_vertices():
            return {
                "success": False,
                "route": [],
                "simulation_steps": [],
                "final_donkey_state": None,
                "total_stars_visited": 0,
                "total_energy_spent": 0,
                "message": f"Estrella inicial {start_star_id} no existe en el grafo"
            }
        
        # Simulador con configuración
        simulator = RouteSimulator(self.star_graph, donkey, self.star_map)
        if research_config:
            simulator.set_research_config(research_config)

        initial_donkey = self._clone_donkey(donkey)
        initial_donkey.visit_star(start_star_id)

        priority = -(1* 1000) + 0 #Estrella visitada, 0 energía gastada

        priority_queue = [(
            priority,
            1,
            0,
            start_star_id,
            [start_star_id],
            initial_donkey,
            []
        )]

        #Mejor resultado encontrado
        best_result = {
            "stars_visited": 1,
            "route": [start_star_id],
            "energy_spent": 0,
            "donkey_state": initial_donkey.get_report(),
            "simulation_steps": []
        }

        #Set de estados visitados: (star_id, num_visited, energy_spent)
        visited_states = set()
        visited_states.add((start_star_id, 1))

        #Contador de iteraciones
        max_iterations = 10000
        iteration = 0

        while priority_queue and iteration < max_iterations:
            iteration += 1

            priority, num_visited, energy_spent, current_star, path, current_donkey, steps = heapq.heappop(priority_queue)

            #Actualizar mejor resultado si encontramos más estrellas
            if num_visited > best_result["stars_visited"]:
                best_result = {
                    "stars_visited": num_visited,
                    "route": path.copy(),
                    "energy_spent": energy_spent,
                    "donkey_state": current_donkey.get_report(),
                    "simulation_steps": steps.copy()
                }
            elif num_visited == best_result["stars_visited"] and energy_spent < best_result["energy_spent"]:
                #Mismo número de estrellas, pero menos energía gastada
                best_result = {
                    "stars_visited": num_visited,
                    "route": path.copy(),
                    "energy_spent": energy_spent,
                    "donkey_state": current_donkey.get_report(),
                    "simulation_steps": steps.copy()
                }

            #Explorar vecinos
            neighbors = self.star_graph.get_neighbors_with_distance(current_star)

            for neighbor_id, distance in neighbors:
                #Evitar revisar estrellas
                if neighbor_id in path:
                    continue

                # Clonar burro para simulación
                test_donkey = self._clone_donkey(current_donkey)

                #Simular visita a la estrella vecina
                visit_result = simulator.simulate_star_visit(test_donkey, current_star, neighbor_id)

                #Si murió, no continuar con la rama
                if not visit_result["success"]:
                    continue

                #Calcular nueva energía gastada
                initial_energy = current_donkey.energy
                final_energy = test_donkey.energy
                energy_consumed = initial_energy - final_energy
                new_energy_spent = energy_spent + energy_consumed

                new_path = path + [neighbor_id]
                new_steps = steps + [visit_result]
                new_num_visited = num_visited + 1

                # Estado para evitar ciclos
                state = (neighbor_id, new_num_visited)
                if state in visited_states:
                    continue
                visited_states.add(state)

                #Calcular prioridad (maximizar estrellas, minimizar energía)
                new_priority = -(new_num_visited * 1000) + new_energy_spent

                #Agregar a la cola
                heapq.heappush(
                    priority_queue,
                    (
                        new_priority,
                        new_num_visited,
                        new_energy_spent,
                        neighbor_id,
                        new_path,
                        test_donkey,
                        new_steps
                    )
                )

        #Retornar el mejor resultado
        return {
            "success": True,
            "route": best_result["route"],
            "simulation_steps": best_result["simulation_steps"],
            "final_donkey_state": best_result["donkey_state"],
            "total_stars_visited": best_result["stars_visited"],
            "total_energy_spent": best_result["energy_spent"],
            "message": f"Ruta óptima encontrada: {best_result['stars_visited']} estrellas visitadas"
        }
    
    def _clone_donkey(self, original_donkey):
        """
        Crea una copia independiente del burro para simulaciones.
        
        Args:
            original_donkey: Burro original
            
        Returns:
            Nueva instancia de Donkey con los mismos valores
        """
        from ..models.donkey import Donkey
        
        cloned = Donkey(
            initial_energy=original_donkey.energy,
            health_state=original_donkey.health_state,
            grass_kg=original_donkey.grass_kg,
            start_age=original_donkey.start_age,
            death_age=original_donkey.death_age
        )
        
        # Copiar estado actual
        cloned.current_age = original_donkey.current_age
        cloned.visited_stars = original_donkey.visited_stars.copy()
        cloned.total_distance_traveled = original_donkey.total_distance_traveled
        cloned.grass_consumed = original_donkey.grass_consumed.copy()
        cloned.research_time = original_donkey.research_time.copy()
        
        return cloned