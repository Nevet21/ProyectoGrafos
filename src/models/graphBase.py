class graphBase:
    def __init__(self):
        # Usamos un diccionario que mapea cada vértice (id_estrella)
        # a otro diccionario con vecinos y pesos.
        # Ejemplo: { 1: {2: 120, 4: 87}, 2: {1: 120, 3: 17} }
        self.adjacency_list = {}

    def add_vertex(self, star_id):
        #Ahora añade un vértice si no existe, si ya existe, no hace nada
        if star_id not in self.adjacency_list:
            self.adjacency_list[star_id] = {}

    def add_edge(self, from_star, to_star, distance):
        #Nos aseguramos de que ambos vértices existen en el grafo
        self.add_vertex(from_star)
        self.add_vertex(to_star)
        #Miramos que sea un grafo no dirigido
        self.adjacency_list[from_star][to_star] = distance
        self.adjacency_list[to_star][from_star] = distance

    def get_neighbors(self, star_id):
        #Devuelve el diccionario con los vecinos con sus distancias,
        #Si no hay vecinos, devuelve el diccionario vacío
        return self.adjacency_list.get(star_id, {})
    
    def get_vertices(self):
        #Devuelve una lista con todos los vértices del grafo
        return list(self.adjacency_list.keys())
    
    def __repr__(self):
        #Funciona como un debug 
        return "\n".join([f"{k}: {v}" for k, v in self.adjacency_list.items()])


