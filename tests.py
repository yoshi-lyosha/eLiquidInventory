import unittest

from eLiquid import ELiquid
from flavor import Flavor
from user import User


class ELiquidEquationTestCase(unittest.TestCase):
    def test_attributes(self):
        strawberry = ELiquid('strawberry', {'1': 1, '2': 2, '3': 3})
        self.assertEqual(strawberry.name, 'strawberry')
        self.assertEqual(strawberry.ingredients, {'1': 1, '2': 2, '3': 3})


class FlavorEquationTestCase(unittest.TestCase):
    def test_attributes(self):
        strawberry_by_tpa = Flavor('strawberry', 'TPA')
        self.assertEqual(strawberry_by_tpa.name, 'strawberry')
        self.assertEqual(strawberry_by_tpa.made_by, 'TPA')


class UserEquationTestCase(unittest.TestCase):
    def test_user_behaviour(self):
        ELiquids_list = []
        user1 = User('Fedos')
        dragon_blood = ELiquid('dragon blood', {'strawberry': 1, 'vanilla': 1})
        strawberry = ELiquid('strawberry', {'strawberry': 1, 'guano': 2})
        ELiquids_list.append(dragon_blood)
        ELiquids_list.append(strawberry)
        user1.add_flavor('strawberry', 1)
        user1.add_flavor('vanilla', 1)
        user1.add_flavor('huila', 1)
        self.assertEqual(user1.show_flavors(), {'strawberry': 1, 'vanilla': 1, 'huila': 1})
        self.assertEqual(user1.show_available_liquid_recipes(ELiquids_list), ['dragon blood'])

if __name__ == '__main__':
    unittest.main()