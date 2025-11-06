class Star:
    def __init__(self, star_id, name, x, y):
        self.star_id = star_id
        self.name = name
        self.x = x
        self.y = y

    # Getters
    def get_star_id(self):
        return self.star_id
    
    def get_name(self):
        return self.name
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    # Setters
    def set_star_id(self, star_id):
        self.star_id = star_id
    
    def set_name(self, name):
        self.name = name
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y