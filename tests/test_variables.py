import unittest

from fastapi.testclient import TestClient

from app.api import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_get_question(self):
        # When
        response = self.client.get("/variables/22d7bdb0-2172-11e4-813c-005056900044")
        # Then
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

    def test_get_non_existing_variable_returns_error(self):
        # When
        response = self.client.get("/variables/non-valid-id")
        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": "Variable uuid 'non-valid-id' was not found"
            }
        )

    def test_get_counts_of_answers_for_non_existing_variable_returns_error(self):
        # When
        response = self.client.get("/variables/non-valid-id/counts")
        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": "Variable uuid 'non-valid-id' was not found"
            }
        )

    def test_get_counts_of_answers_when_there_are_no_answers(self):
        # When
        response = self.client.get("/variables/015dbd00-a4f6-11e7-9f92-d298beabf694/counts")
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "1": 0,
                "2": 0,
                "3": 0,
            }
        )

    def test_get_counts_of_answers(self):
        # When
        response = self.client.get("/variables/22d7bdb0-2172-11e4-813c-005056900044/counts")
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "1": 195,
                "2": 224,
                "3": 32,
                "4": 9
            }
        )
