import sqlalchemy
from website.app import db, models

class Storage:
    def __init__(self, storage_source):
        self.storage = storage_source

    def check_flavor_exists(self, flavor_name, made_by):
        return flavor_name in self.storage

    def check_liquid_exists(self, eliquid_name, made_by):
        return eliquid_name in self.storage

    def add_new_flavor(self, flavor_name, made_by):
        new_flavor = models.Flavoring(flavoring_name=flavor_name, producer_name=made_by)
        self.storage.session.add(new_flavor)
        self.storage.session.commit()

    def add_new_eliquid(self, eliquid_name, made_by):
        self.storage.add(eliquid_name, made_by)

    def show_flavors(self):
        print(models.Flavoring.query.all())


if __name__ == '__main__':
    my_storage = Storage(db)
    print(my_storage)
    my_storage.show_flavors()
    my_storage.add_new_flavor('sadasd', 'TPA')
    my_storage.show_flavors()