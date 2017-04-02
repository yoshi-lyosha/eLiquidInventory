class ELiquid:

    def __init__(self, name, ingredients_dict=None):
        self.name = name
        if not ingredients_dict:
            self.ingredients = {}
        self.ingredients = ingredients_dict

    def set_ingredients(self, ingredients_dict):
        self.ingredients = ingredients_dict

    def add_ingredient(self, ingredient, quantity):
        self.ingredients[ingredient] = quantity

    def delete_ingredient(self, ingredient):
        del self.ingredients[ingredient]
