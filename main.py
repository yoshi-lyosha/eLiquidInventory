from eLiquid import ELiquid
from user import User


# def output_available_recipes(user, ELiquids_list):
#     for ELiquid in user.show_available_liquid_recipes(ELiquids_list):
#         print(ELiquid.name, ELiquid.ingredients)

if __name__ == '__main__':
    ELiquids_list = []
    user1 = User('Fedos')
    dragon_blood = ELiquid('dragon blood', ['strawberry', 'vanilla'])
    ELiquids_list.append(dragon_blood)
    strawberry = ELiquid('strawberry', ['strawberry', 'guano'])
    ELiquids_list.append(strawberry)
    user1.add_flavor('strawberry')
    user1.add_flavor('vanilla')
    user1.add_flavor('huila')
    user1.show_flavors()
    user1.show_available_liquid_recipes(ELiquids_list)