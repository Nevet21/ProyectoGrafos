
class Relation:
    def __init__(self, id_relation, name, starA, starB):
        self.id_relation = id_relation
        self.name = name
        self.starA = starA
        self.starB = starB
    
    # Getters
    def get_id_relation(self):
        return self.id_relation
    
    def get_name(self):
        return self.name
    
    def get_starA(self):
        return self.starA
    
    def get_starB(self):
        return self.starB
    
    # Setters
    def set_id_relation(self, id_relation):
        self.id_relation = id_relation
    
    def set_name(self, name):
        self.name = name
    
    def set_starA(self, starA):
        self.starA = starA
    
    def set_starB(self, starB):
        self.starB = starB
        
    def distance(self):
        distanceX=self.starA.x-self.starB.x
        distanceY=self.starA.y-self.starB.y
        print(distanceX)