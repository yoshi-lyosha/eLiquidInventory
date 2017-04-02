import sqlalchemy

class Storage:
    def __init__(self, storage_source):
        self.storage = storage_source

    def check_flavor_exists(self, flavor_name, made_by):
        return flavor_name in self.storage

    def check_liquid_exists(self, eliquid_name, made_by):
        return eliquid_name in self.storage

    def add_new_flavor(self, flavor_name, made_by):
        self.storage.add(flavor_name, made_by)

    def add_new_eliquid(self, eliquid_name, made_by):
        self.storage.add(eliquid_name, made_by)
