class User:

    def __init__(self, name):
        self.name = name
        self.flavors = {}
        self.favorites = []

    def show_available_liquid_recipes(self, eliquids_list):
        available_recipes = []
        for ELiquid in eliquids_list:
            # print(ELiquid.__dict__)
            # print(ELiquid.ingredients)
            ingredients_quantity = len(ELiquid.ingredients)
            for ingredient, quantity in ELiquid.ingredients.items():
                if ingredient in self.flavors:
                    if quantity <= self.flavors.get(ingredient):
                        ingredients_quantity -= 1
            if ingredients_quantity == 0:
                available_recipes.append(ELiquid.name)
        return available_recipes

    def add_flavor(self, flavor_name, quantity):
        self.flavors[flavor_name] = quantity

    def edit_flavor(self, flavor_name, new_quantity):
        self.flavors[flavor_name] = new_quantity
        
    def show_flavors(self):
        return self.flavors

    def add_to_favorites(self, eliquid):
        self.favorites.append(eliquid)

    def delete_from_favorites(self, eliquid):
        self.favorites.remove(eliquid)

    def show_favorites(self):
        return self.favorites
