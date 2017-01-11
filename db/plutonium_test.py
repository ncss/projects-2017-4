import unittest

class TestPlutonium(unittest.TestCase):

    def setUp(self):
        pass
        
    def test_animals(self):
        self.assertEqual( 'Giraffe', 'Giraffe' )
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()