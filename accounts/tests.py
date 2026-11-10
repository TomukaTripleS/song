from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from music.models import Artist

User = get_user_model()
PASSWORD = "study-password-2026"


class AccountsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="student", password=PASSWORD)
        cls.artist = Artist.objects.create(name="Виконавець")

    def test_registration(self):
        response = self.client.post("/api/register/", {
            "username": "newuser", "email": "new@example.com",
            "password": PASSWORD, "password_confirmation": PASSWORD,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="newuser")
        self.assertTrue(user.check_password(PASSWORD))
        self.assertNotEqual(user.password, PASSWORD)
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertNotIn("password", response.data)
        self.assertNotIn("password_confirmation", response.data)

    def test_registration_errors(self):
        response = self.client.post("/api/register/", {
            "username": "", "email": "invalid", "password": "short",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data["error"]["details"]), {
            "username", "email", "password", "password_confirmation",
        })
        response = self.client.post("/api/register/", {
            "username": "newuser", "email": "new@example.com",
            "password": PASSWORD, "password_confirmation": "different-password",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password_confirmation", response.data["error"]["details"])
        response = self.client.post("/api/register/", {
            "username": "ｓtudent", "email": "new@example.com",
            "password": PASSWORD, "password_confirmation": PASSWORD,
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data["error"]["details"])
        self.assertEqual(User.objects.count(), 1)

    def test_login_and_profile(self):
        response = self.client.post("/api/token/", {
            "username": "student", "password": PASSWORD,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {"access", "refresh"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        profile = self.client.get("/api/me/")
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.data["username"], "student")

    def test_wrong_password(self):
        response = self.client.post("/api/token/", {
            "username": "student", "password": "wrong",
        }, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.data["error"]["message"])

    def test_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        access.set_exp(lifetime=timedelta(seconds=-1))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(self.client.get("/api/me/").status_code, 401)
        response = self.client.post("/api/token/refresh/", {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(self.client.get("/api/me/").status_code, 200)
        response = self.client.post("/api/token/refresh/", {"refresh": "invalid"}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_permissions(self):
        self.assertEqual(self.client.get("/api/songs/").status_code, 200)
        self.assertEqual(self.client.get("/api/me/").status_code, 401)
        song = {
            "title": "Пісня", "artist": self.artist.pk,
            "genre": "Рок", "listen_url": "https://example.com/song",
        }
        self.assertEqual(self.client.post("/api/songs/", song, format="json").status_code, 401)
        access = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        created = self.client.post("/api/songs/", song, format="json")
        self.assertEqual(created.status_code, 201)
        url = f"/api/songs/{created.data['id']}/"
        self.client.credentials()
        self.assertEqual(self.client.patch(url, {"title": "Змінено"}, format="json").status_code, 401)
        self.assertEqual(self.client.delete(url).status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(self.client.patch(url, {"title": "Змінено"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)
