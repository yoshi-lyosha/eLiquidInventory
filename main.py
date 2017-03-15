from eLiquid import ELiquid


if __name__ == '__main__':
    dragonblood = ELiquid("Dragon blood")
    print(dragonblood.name)
    dragonblood.set_ingredients(['sweet', 'shit', 'dragon', 'strawberry'])
    print(dragonblood.ingredients)
    print(dragonblood)