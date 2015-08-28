__author__ = 'cloud'

import unittest


class TestPromise(unittest.TestCase):
    def testPromise(self):
        pass

    def test2(self):
        print('test2')


suite = unittest.TestSuite()
# suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPromise))
suite.addTests(unittest.TestLoader().loadTestsFromModule(__name__))

if __name__ == '__main__':
    unittest.main(defaultTest=suite)
