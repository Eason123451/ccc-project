import unittest
from get_url_data import get_url_data

class TestGetUrlData(unittest.TestCase):
    def test_incorrect_endpoint(self):
        """ Test handling of incorrect endpoint. """
        data = get_url_data(9088, 'nonexistent-endpoint')
        self.assertIsNone(data, "The function should return None when the endpoint does not exist.")
    
    def test_wrong_port(self):
        """ Test the function with an incorrect port. """
        data = get_url_data(9999, 'search-twitter-daily-tweets')  # Assuming 9999 is incorrect
        self.assertIsNone(data, "The function should return None when it cannot connect to the server.")

if __name__ == '__main__':
    unittest.main()

