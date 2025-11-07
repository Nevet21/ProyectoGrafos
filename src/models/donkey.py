"""
Modelo del Burro (Donkey)
Representa al burro que viaja por las estrellas
"""

class Donkey:
    """
    Clase que representa al burro espacial que viaja entre estrellas.
    Maneja su energía, salud, pasto y tiempo de vida.
    """
    
    # Estados de salud posibles
    HEALTH_STATES = {
        "Excelente": {"min_energy": 75, "energy_per_kg": 5},
        "Buena": {"min_energy": 50, "energy_per_kg": 3},
        "Mala": {"min_energy": 25, "energy_per_kg": 2},
        "Moribundo": {"min_energy": 1, "energy_per_kg": 1},
        "Muerto": {"min_energy": 0, "energy_per_kg": 0}
    }
    
    def __init__(self, initial_energy=100, health_state="Excelente", 
                 grass_kg=300, start_age=12, death_age=3567):
        """
        Inicializa el burro con sus parámetros.
        
        Args:
            initial_energy: Energía inicial (0-100%)
            health_state: Estado de salud inicial
            grass_kg: Kilogramos de pasto disponible
            start_age: Edad inicial en años luz
            death_age: Edad de muerte en años luz
        """
        self.energy = initial_energy  # 0-100%
        self.health_state = health_state
        self.grass_kg = grass_kg
        self.start_age = start_age  # Edad inicial (para algoritmos)
        self.current_age = start_age  # Edad actual durante el viaje
        self.death_age = death_age
        
        # Historial del viaje
        self.visited_stars = []  # Lista de IDs de estrellas visitadas
        self.total_distance_traveled = 0
        self.grass_consumed = {}  # {star_id: kg_consumed}
        self.research_time = {}  # {star_id: time_spent}
        
    def is_alive(self):
        """Verifica si el burro está vivo"""
        return self.health_state != "Muerto" and self.current_age < self.death_age
    
    def get_remaining_life(self):
        """Retorna el tiempo de vida restante en años luz"""
        return max(0, self.death_age - self.current_age)
    
    def can_eat(self):
        """Verifica si el burro puede comer (tiene menos del 50% de energía)"""
        return self.energy < 50
    
    def eat(self, star_time_to_eat, max_time_available=None):
        """
        El burro come pasto en una estrella.
        
        Args:
            star_time_to_eat: Tiempo que tarda en comer 1 kg de pasto en esta estrella
            max_time_available: Tiempo máximo disponible para comer (50% del tiempo en estrella)
            
        Returns:
            dict con información del proceso: {kg_eaten, energy_gained, time_spent}
        """
        if not self.can_eat() or self.grass_kg <= 0:
            return {"kg_eaten": 0, "energy_gained": 0, "time_spent": 0}
        
        # Energía que necesitamos para llegar al 100%
        energy_needed = 100 - self.energy
        
        # Energía por kg según estado de salud
        energy_per_kg = self.HEALTH_STATES[self.health_state]["energy_per_kg"]
        
        # Kilogramos necesarios
        kg_needed = energy_needed / energy_per_kg
        
        # Kilogramos que podemos comer (limitado por pasto disponible)
        kg_to_eat = min(kg_needed, self.grass_kg)
        
        # Tiempo que tomaría comer todo lo necesario
        time_needed = kg_to_eat * star_time_to_eat
        
        # Si hay límite de tiempo, ajustar
        if max_time_available is not None and time_needed > max_time_available:
            time_needed = max_time_available
            kg_to_eat = max_time_available / star_time_to_eat
        
        # Realizar la comida
        energy_gained = kg_to_eat * energy_per_kg
        self.energy = min(100, self.energy + energy_gained)
        self.grass_kg -= kg_to_eat
        
        return {
            "kg_eaten": kg_to_eat,
            "energy_gained": energy_gained,
            "time_spent": time_needed
        }
    
    def travel(self, distance_light_years):
        """
        Viaja entre estrellas, consume tiempo de vida.
        
        Args:
            distance_light_years: Distancia a viajar en años luz
            
        Returns:
            bool: True si sobrevivió el viaje, False si murió
        """
        self.current_age += distance_light_years
        self.total_distance_traveled += distance_light_years
        
        # Verificar si murió de viejo
        if self.current_age >= self.death_age:
            self.health_state = "Muerto"
            return False
        
        return True
    
    def do_research(self, time_spent, energy_cost_per_time):
        """
        Realiza investigación en una estrella, consume energía.
        
        Args:
            time_spent: Tiempo invertido en investigación
            energy_cost_per_time: Energía consumida por unidad de tiempo
            
        Returns:
            bool: True si completó la investigación, False si se quedó sin energía
        """
        energy_consumed = time_spent * energy_cost_per_time
        self.energy -= energy_consumed
        
        # Si la energía llega a 0 o menos, el burro muere
        if self.energy <= 0:
            self.energy = 0
            self.health_state = "Muerto"
            return False
        
        # Actualizar estado de salud según energía
        self._update_health_state()
        
        return True
    
    def visit_star(self, star_id):
        """Registra la visita a una estrella"""
        if star_id not in self.visited_stars:
            self.visited_stars.append(star_id)
    
    def has_visited(self, star_id):
        """Verifica si ya visitó una estrella"""
        return star_id in self.visited_stars
    
    def record_grass_consumption(self, star_id, kg_consumed):
        """Registra cuánto pasto consumió en una estrella"""
        if star_id not in self.grass_consumed:
            self.grass_consumed[star_id] = 0
        self.grass_consumed[star_id] += kg_consumed
    
    def record_research_time(self, star_id, time_spent):
        """Registra cuánto tiempo investigó en una estrella"""
        if star_id not in self.research_time:
            self.research_time[star_id] = 0
        self.research_time[star_id] += time_spent
    
    def use_hypergiant_portal(self):
        """
        Usa el portal de una estrella hipergigante.
        Recarga 50% de energía y duplica el pasto.
        """
        # Recargar 50% de la energía actual
        self.energy = min(100, self.energy * 1.5)
        
        # Duplicar pasto
        self.grass_kg *= 2
    
    def _update_health_state(self):
        """Actualiza el estado de salud según la energía actual"""
        if self.energy >= 75:
            self.health_state = "Excelente"
        elif self.energy >= 50:
            self.health_state = "Buena"
        elif self.energy >= 25:
            self.health_state = "Mala"
        elif self.energy > 0:
            self.health_state = "Moribundo"
        else:
            self.health_state = "Muerto"
    
    def get_report(self):
        """
        Genera un reporte completo del viaje.
        
        Returns:
            dict con toda la información del viaje
        """
        return {
            "energy": self.energy,
            "health_state": self.health_state,
            "grass_kg": self.grass_kg,
            "current_age": self.current_age,
            "death_age": self.death_age,
            "remaining_life": self.get_remaining_life(),
            "visited_stars": self.visited_stars.copy(),
            "total_stars_visited": len(self.visited_stars),
            "total_distance_traveled": self.total_distance_traveled,
            "grass_consumed": self.grass_consumed.copy(),
            "research_time": self.research_time.copy(),
            "is_alive": self.is_alive()
        }
    
    def __repr__(self):
        """Representación en string del burro"""
        return (f"Donkey(energy={self.energy:.1f}%, health={self.health_state}, "
                f"grass={self.grass_kg:.1f}kg, age={self.current_age:.1f}/{self.death_age})")
