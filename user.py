class User:

    def __init__(self, name):
        self.name = name
        self.flavors = set()

    def show_available_liquid_recipes(self, ELiquids_list):
        available_recipes = []
        for ELiquid in ELiquids_list:
            if ELiquid.ingredients & self.flavors == ELiquid.ingredients:
                available_recipes.append(ELiquid.name)
        print("{user_name} can mix eLiquids: {available_recipes}".format(user_name=self.name, available_recipes=available_recipes))

    def add_flavor(self, flavor_name):
        self.flavors.add(flavor_name)

    def show_flavors(self):
        print("{user_name} has flavors: {flavors}".format(user_name=self.name, flavors=self.flavors))