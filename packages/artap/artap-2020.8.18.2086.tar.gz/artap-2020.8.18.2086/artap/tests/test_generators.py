import unittest
from ..operators import CustomGenerator, RandomGenerator, FullFactorGenerator, PlackettBurmanGenerator, \
    BoxBehnkenGenerator, LHSGenerator


class TestDOE(unittest.TestCase):

    def setUp(self):
        self.parameters = [{'name': 'x_1', 'initial_value': 2.5, 'bounds': [-2.5, 5]},
                           {'name': 'x_2', 'initial_value': 1.5, 'bounds': [1, 3.4]},
                           {'name': 'x_3', 'initial_value': 3.5, 'bounds': [6, 10]}]

    def test_random_generator(self):
        gen = RandomGenerator(parameters=self.parameters)
        gen.init(3)
        individuals = gen.generate()
        # values
        self.assertTrue(self.parameters[0]['bounds'][0] <= individuals[0].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[0].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[0].vector[2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= individuals[1].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[1].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[1].vector[2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= individuals[2].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[2].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[2].vector[2] <= self.parameters[2]['bounds'][1])

    def test_custom_generator(self):
        gen = CustomGenerator()
        gen.init([[3, 2, 6], [-1, 3, 8]])
        individuals = gen.generate()
        # values
        self.assertEqual(individuals[0].vector[0], 3)
        self.assertEqual(individuals[0].vector[1], 2)
        self.assertEqual(individuals[0].vector[2], 6)
        self.assertEqual(individuals[1].vector[0], -1)
        self.assertEqual(individuals[1].vector[1], 3)
        self.assertEqual(individuals[1].vector[2], 8)

    # Factorial Designs
    def test_full_fact_generator(self):
        # General Full-Factorial
        gen = FullFactorGenerator(parameters=self.parameters)
        gen.init(center=False)
        individuals = gen.generate()

        # size
        self.assertEqual(len(individuals), 8)
        # values
        self.assertEqual(individuals[0].vector[0], -2.5)
        self.assertEqual(individuals[1].vector[0], 5.0)
        self.assertEqual(individuals[2].vector[1], 3.4)
        self.assertEqual(individuals[3].vector[1], 3.4)
        self.assertEqual(individuals[7].vector[2], 10.0)

        gen = FullFactorGenerator(parameters=self.parameters)
        gen.init(center=True)
        individuals = gen.generate()

        self.assertEqual(individuals[3].vector[0], -2.5)
        self.assertEqual(individuals[-1].vector[1], 3.4)

    def test_plackett_burman_generator(self):
        # Plackett-Burman
        gen = PlackettBurmanGenerator(parameters=self.parameters)
        individuals = gen.generate()

        # size
        self.assertEqual(len(individuals), 4)
        # values
        self.assertEqual(individuals[0].vector[0], -2.5)
        self.assertEqual(individuals[1].vector[0], 5.0)
        self.assertEqual(individuals[2].vector[2], 6.0)
        self.assertEqual(individuals[3].vector[1], 3.4)

    # Response - Surface Designs
    def test_box_behnken_generator(self):
        # Box-Behnken
        gen = BoxBehnkenGenerator(parameters=self.parameters)
        individuals = gen.generate()

        # size
        self.assertEqual(len(individuals), 13)
        # values
        self.assertEqual(individuals[2].vector[2], 8.0)
        self.assertEqual(individuals[3].vector[1], 3.4)
        self.assertEqual(individuals[5].vector[0], 5.0)
        self.assertEqual(individuals[12].vector[1], 2.2)

    # Randomized Designs
    def test_lhs_generation(self):
        # Latin - Hypercube
        gen = LHSGenerator(parameters=self.parameters)
        gen.init(number=3)
        individuals = gen.generate()

        # size
        self.assertEqual(len(individuals), 3)
        # values
        self.assertTrue(self.parameters[0]['bounds'][0] <= individuals[0].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[0].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[0].vector[2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= individuals[1].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[1].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[1].vector[2] <= self.parameters[2]['bounds'][1] and
                        self.parameters[0]['bounds'][0] <= individuals[2].vector[0] <= self.parameters[0]['bounds'][1] and
                        self.parameters[1]['bounds'][0] <= individuals[2].vector[1] <= self.parameters[1]['bounds'][1] and
                        self.parameters[2]['bounds'][0] <= individuals[2].vector[2] <= self.parameters[2]['bounds'][1])


if __name__ == '__main__':
    unittest.main()
