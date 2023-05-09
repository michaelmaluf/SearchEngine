import unittest
from search_engine import clean_str, search, app


class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_clean_str(self):
        test_str = "This is a t3st string With @weird* characters."
        expected_output = "this is a t3st string with weird characters"
        self.assertEqual(clean_str(test_str), expected_output)

    def test_search_empty_query(self):
        query = ""
        expected_output = []
        self.assertEqual(search(query), expected_output)

    def test_search_non_empty_query(self):
        query = "Python language"
        expected_output = [
            {
                "id": 1,
                "username": "user1",
                "content": "Python is an overrated language, but I still respect it.",
                "score": 3.991226075692495
            }
        ]
        self.assertEqual(search(query), expected_output)

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
