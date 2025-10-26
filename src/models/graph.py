class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent

    def get_id(self):
        return self.id
    
class Graph:
    def __init__(self):
        self.vertex_list = {}
        self.num_vertex = 0

    def add_vertex(self, id):
        self.num_vertex += 1
        new_vertex = Vertex(id)
        self.vertex_list[id] = new_vertex
        return new_vertex

    def get_vertex(self, id):
        return self.vertex_list.get(id)

    def add_edge(self, from_id, to_id, weight=0):
        if from_id not in self.vertex_list:
            self.add_vertex(from_id)
        if to_id not in self.vertex_list:
            self.add_vertex(to_id)
        self.vertex_list[from_id].add_neighbor(to_id, weight)

    def get_vertices(self):
        return self.vertex_list.keys()