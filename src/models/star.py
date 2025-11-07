class Star:
    def __init__(self, star_id, name, x, y, time_to_eat_kg=1.0, energy_cost_research=0.5,
                 health_impact=0, lifespan_change=0, is_hypergiant=False, max_stay_time=100):

       #Propiedades básicas 
        self.star_id = star_id
        self.name = name
        self.x = x
        self.y = y

        #Propiedades de simulación
        self.time_to_eat_kg = time_to_eat_kg  # Tiempo para comer 1 kg de pasto
        self.energy_cost_research = energy_cost_research  # Energía consumida por unidad de tiempo de investigación
        self.health_impact = health_impact  # Impacto en la salud del burro
        self.lifespan_change = lifespan_change  # Cambio en la esperanza de vida
        self.is_hypergiant = is_hypergiant  # Si es una estrella hipergigante
        self.max_stay_time = max_stay_time  # Tiempo máximo de permanencia

    # Getters
    def get_star_id(self):
        return self.star_id
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_time_to_eat_kg(self):
        return self.time_to_eat_kg
    
    def get_energy_cost_research(self):
        return self.energy_cost_research
    
    def get_health_impact(self):
        return self.health_impact
    
    def get_lifespan_change(self):
        return self.lifespan_change
    
    def get_is_hypergiant(self):
        return self.is_hypergiant
    
    def get_max_stay_time(self):
        return self.max_stay_time
    
    # Setters
    def set_star_id(self, star_id):
        self.star_id = star_id
    
    def set_name(self, name):
        self.name = name
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y

    def set_time_to_eat_kg(self, time_to_eat_kg):
        self.time_to_eat_kg = time_to_eat_kg

    def set_energy_cost_research(self, energy_cost_research):
        self.energy_cost_research = energy_cost_research

    def set_health_impact(self, health_impact):
        self.health_impact = health_impact

    def set_lifespan_change(self, lifespan_change):
        self.lifespan_change = lifespan_change

    def set_is_hypergiant(self, is_hypergiant):
        self.is_hypergiant = is_hypergiant

    def set_max_stay_time(self, max_stay_time):
        self.max_stay_time = max_stay_time


    def __repr__(self):
        return (f"Star(id={self.star_id}, name='{self.name}', x={self.x}, y={self.y}, "
                f"pos=({self.x}, {self.y}), hypergiant={self.is_hypergiant})")