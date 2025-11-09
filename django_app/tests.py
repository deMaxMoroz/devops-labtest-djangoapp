from django.test import TestCase, Client

class BasicTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_api_endpoint(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("hostname", data)
        self.assertIn("database", data)

    def test_create_and_get_notes(self):
        response = self.client.post(
            "/notes/",
            data='{"text":"test note"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        note_id = response.json()["id"]

        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        notes = response.json()["notes"]
        ids = [n["id"] for n in notes]
        self.assertIn(note_id, ids)
