import unittest

from fastapi.testclient import TestClient

from app.api import app


class ApiTests(unittest.TestCase):
    def test_get_question(self):
        client = TestClient(app)
        response = client.get("/variables/22d7bdb0-2172-11e4-813c-005056900044")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "label": "Personality - Express feelings or keep to yourself",
                "options": [
                    {
                        "code": 1,
                        "label": "I readily express my feelings",
                        "option": "1"
                    },
                    {
                        "code": 2,
                        "label": "I tend to keep my feelings to myself",
                        "option": "2"
                    },
                    {
                        "code": 3,
                        "label": "Neither",
                        "option": "3"
                    },
                    {
                        "code": 4,
                        "label": "Don’t know",
                        "option": "4"
                    }
                ],
                "question": "Would you say you readily express your feelings, or tend to keep them to yourself?",
                "type": "list-single",
                "uuid": "22d7bdb0-2172-11e4-813c-005056900044"
            }
        )
