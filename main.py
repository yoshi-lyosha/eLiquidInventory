from eLiquid import ELiquid
from user import User


if __name__ == '__main__':
    user1 = User('Fedos')
    user2 = User('Koresh')
    user3 = User('Olga')
    dragonblood = ELiquid("Dragon blood")
    print(dragonblood.name)
    dragonblood.set_ingredients(['sweet', 'shit', 'dragon', 'strawberry'])
    print(dragonblood.ingredients)
    print(dragonblood)
    user1.add_flavor('strawberry')
    print(user1.name, user1.flavors)