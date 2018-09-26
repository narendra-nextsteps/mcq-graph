import unittest

import graph_curation


class Graph_curationTestCase(unittest.TestCase):

    def test_sample(self):
        self.assertIn('Hi cookiecutter, Welcome to graph_curation', graph_curation.sample())


if __name__ == '__main__':
    unittest.main()
