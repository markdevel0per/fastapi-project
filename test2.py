import unittest
from fastapi.testclient import TestClient
from main import app


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_submit_city(self):
        response = self.client.post('/submit', data={"user_input": "London"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_weather(self):
        response = self.client.get('/weather/London')
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])

    def test_get_my_history(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])


if __name__ == '__main__':
    unittest.main()
