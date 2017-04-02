import unittest

from eLiquid import ELiquid


class eLiquidEquationTestCase(unittest.TestCase):
    def test_attributes(self):
        strawberry = ELiquid('strawberry', ['1', '2', '3'])
        self.assertEqual(strawberry.name, 'strawberry')
        self.assertEqual(strawberry.ingredients, {'1', '2', '3'})

if __name__ == '__main__':
    unittest.main()