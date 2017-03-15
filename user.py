class User:

    def __init__(self, name):
        self.name = name
        self.flavors = []

    def show_available_liquid_recipes(self):
        pass

    def add_flavor(self, flavor_name):
        self.flavors.append(flavor_name)