"""
RouteSimulator - Simulación completa del viaje del burro (Requisito 3)
Simula todas las mecánicas: comer, investigar, viajar, hipergigantes
"""

from typing import Dict, List, Tuple, Any, Optional

class RouteSimulator:
    """
    Simula el viaje completo del burro entre estrellas.
    Maneja: comida, investigación, viaje, hipergigantes, muerte.
    """

    def __init__(self, star_graph, donkey, star_map):
        """
        Inicializa el simulador.
        
        Args:
            star_graph: Instancia de StarGraph
            donkey: Instancia de Donkey (se clonará para simulaciones)
            star_map: Diccionario con info de todas las estrellas
        """
        self.star_graph = star_graph
        self.donkey = donkey
        self.star_map = star_map

        self.research_config = {}

    def set_research_config(self, config: Dict[int, Dict[str, Any]]):
        """
        Configura los parámetros de investigación por estrella.
        
        Args:
            config: Diccionario {star_id: {research parameters}}
        """
        self.research_config = config

    def simulate_star_visit(self, donkey, current_star_id, next_star_id) -> Dict[str, Any]:
        """
        Simula la visita completa a una estrella siguiente.
        
        Proceso:
        1. Viajar desde current_star_id a next_star_id
        2. Si energía < 50%: Comer (máx 50% del tiempo en estrella)
        3. Investigar (resto del tiempo disponible)
        4. Verificar si es hipergigante
        
        Args:
            donkey: Instancia de Donkey (se modifica)
            current_star_id: ID de la estrella actual (None si es la primera)
            next_star_id: ID de la estrella a visitar
            
        Returns:
            dict con toda la información de la visita: {
                "success": bool,
                "star_id": int,
                "travel_result": dict,
                "eat_result": dict,
                "research_result": dict,
                "hypergiant_bonus": dict o None,
                "donkey_state": dict,
                "death_reason": str o None
            }
        """
        result = {
            "success": False,
            "star_id": next_star_id,
            "travel_result": None,
            "eat_result": None,
            "research_result": None,
            "hypergiant_bonus": None,
            "donkey_state": None,
            "death_reason": None
        }

        #1. Viajar a otra estrella
        if current_star_id is not None:
            distance = self.star_graph.get_distance_between(current_star_id, next_star_id)

            if distance is None:
                result["death_reason"] = "No hay conexión entre estrellas"
                # Guardar estado del burro
                result["donkey_state"] = {
                    "energy": donkey.energy,
                    "health_state": donkey.health_state,
                    "grass_kg": donkey.grass_kg,
                    "current_age": donkey.current_age,
                    "death_age": donkey.death_age,
                    "remaining_life": donkey.get_remaining_life(),
                    "is_alive": donkey.is_alive()
                }
                return result
            
            #Consumir años luz al viajar
            travel_success = donkey.travel(distance)
            result["travel_result"] = {
                "distance": distance,
                "success": travel_success,
                "new_age": donkey.current_age
            }

            if not travel_success:
                result["death_reason"] = "El burro murió de anciano"
                # Guardar estado del burro incluso si murió
                result["donkey_state"] = {
                    "energy": donkey.energy,
                    "health_state": donkey.health_state,
                    "grass_kg": donkey.grass_kg,
                    "current_age": donkey.current_age,
                    "death_age": donkey.death_age,
                    "remaining_life": donkey.get_remaining_life(),
                    "is_alive": donkey.is_alive()
                }
                return result
            
        #2. Registrar visita de estrella
        donkey.visit_star(next_star_id)

        #Para obtener datos de la estrella
        star_data = self.star_map.get(next_star_id)
        if not star_data:
            result["death_reason"] = "Estrella no encontrada en el mapa"
            # Guardar estado del burro
            result["donkey_state"] = {
                "energy": donkey.energy,
                "health_state": donkey.health_state,
                "grass_kg": donkey.grass_kg,
                "current_age": donkey.current_age,
                "death_age": donkey.death_age,
                "remaining_life": donkey.get_remaining_life(),
                "is_alive": donkey.is_alive()
            }
            return result

        #3. Comer si burro energía < 50%
        if donkey.can_eat():
            star_time_to_eat = star_data.get("timeToEat", 1)

            # El burro puede invertir máximo 50% del tiempo en comer
            # Asumimos que tiene un tiempo base por estrella (ej: 10 unidades)
            max_eat_time = 5

            eat_result = donkey.eat(star_time_to_eat, max_eat_time)
            result["eat_result"] = eat_result

            #Para registrar el consumo
            if eat_result["kg_eaten"] > 0:
                donkey.record_grass_consumption(next_star_id, eat_result["kg_eaten"])

        else:
            result["eat_result"] = {"kg_eaten":0, "energy-gained":0, "time_spent":0}

        #4 Investigar con lo el tiempo restante
        research_params = self.research_config.get(next_star_id, {
            "research_time": 5,
            "energy_cost_per_time": 1,
            "health_effect": 0,
            "life_effect":0
        })
        
        # Ejecutar la investigación
        research_result = donkey.do_research(
            time_spent=research_params["research_time"],
            energy_cost_per_time=research_params["energy_cost_per_time"],
            health_effect=research_params.get("health_effect", 0),
            life_effect=research_params.get("life_effect", 0)
        )

        result["research_result"] = research_result

        #Registrar tiempo de investigación
        donkey.record_research_time(next_star_id, research_params["research_time"])

        #Verificar si murió durante la investigación
        if not research_result["success"]:
            result["death_reason"] = research_result.get("death_reason", "El burro murió durante la investigación")
            # Guardar estado del burro incluso si murió
            result["donkey_state"] = {
                "energy": donkey.energy,
                "health_state": donkey.health_state,
                "grass_kg": donkey.grass_kg,
                "current_age": donkey.current_age,
                "death_age": donkey.death_age,
                "remaining_life": donkey.get_remaining_life(),
                "is_alive": donkey.is_alive()
            }
            return result
        
        #5. Verificar si es hipergigante
        if star_data.get("hypergiant", False):
            portal_result = donkey.use_hypergiant_portal()
            result["hypergiant_bonus"] = portal_result

        #6. Guardar estado final del burro
        result["donkey_state"] = {
            "energy": donkey.energy,
            "health_state": donkey.health_state,  # Cambiado de "health" a "health_state"
            "grass_kg": donkey.grass_kg,
            "current_age": donkey.current_age,    # Cambiado de "age" a "current_age"
            "death_age": donkey.death_age,         # Agregado para mostrar edad máxima
            "remaining_life": donkey.get_remaining_life(),
            "is_alive": donkey.is_alive()
        }

        result["success"] = donkey.is_alive()
        return result

