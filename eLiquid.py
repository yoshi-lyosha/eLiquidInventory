class ELiquid:


    def __init__(self, name, ingredients_set):
        self.name = name
        self.ingredients = set(ingredients_set)

    def set_ingredients(self, ingredients_set):
        self.ingredients = ingredients_set
