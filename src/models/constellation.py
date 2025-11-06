class Constellation:
    def __init__(self, id_constellation, name):
        self.id_constellation = id_constellation
        self.name = name
    
    # Getters
    def get_id_constellation(self):
        return self.id_constellation
    
    def get_name(self):
        return self.name
    
    # Setters
    def set_id_constellation(self, id_constellation):
        self.id_constellation = id_constellation
    
    def set_name(self, name):
        self.name = name