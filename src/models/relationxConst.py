class RelationxConst:
    def __init__(self, id_relationxConst, relation, constellation):
        self.id_relationxConst = id_relationxConst
        self.relation = relation
        self.constellation = constellation
    
    # Getters
    def get_id_relationxConst(self):
        return self.id_relationxConst
    
    def get_relation(self):
        return self.relation
    
    def get_constellation(self):
        return self.constellation
    
    # Setters
    def set_id_relationxConst(self, id_relationxConst):
        self.id_relationxConst = id_relationxConst
    
    def set_relation(self, relation):
        self.relation = relation
    
    def set_constellation(self, constellation):
        self.constellation = constellation
