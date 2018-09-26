import unittest

import graph_curation_flask


class Graph_curationFlaskViewTestCase(unittest.TestCase):

    def setUp(self):
        self.app = graph_curation_flask.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to graph_curation', rv.data.decode())


class Graph_curationFlaskApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = graph_curation_flask.app.test_client()

    def test_index(self):
        rv = self.app.get('/sample')
        self.assertIn('Hi cookiecutter, Welcome to graph_curation', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
