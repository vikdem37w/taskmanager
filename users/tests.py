from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class unitTest(TestCase):
    def test(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            "/api/tasks/",
            data={
                "title": "testtask",
                "description": "testdescription",
                "status": "in_progress",
                "priority": "medium",
                "due_date": "1999-12-31",
                "user": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 201)
        task_id = response.json()["id"]
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "testtask")
        self.assertEqual(response.json()[0]["description"], "testdescription")
        self.assertEqual(response.json()[0]["status"], "in_progress")
        self.assertEqual(response.json()[0]["priority"], "medium")
        self.assertEqual(response.json()[0]["due_date"], "1999-12-31")
        self.assertEqual(response.json()[0]["user"], self.user.id)
        response = self.client.patch(
            f"/api/tasks/{task_id}/",
            data={"description": "testdescription2"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "testdescription2")
        response = self.client.delete(f"/api/tasks/{task_id}/")
        self.assertEqual(response.status_code, 204)
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)
        self.client.logout()
