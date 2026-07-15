import unittest

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from config import get_settings


class AppConfigTests(unittest.TestCase):
    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_settings_default_to_development(self) -> None:
        settings = get_settings()
        self.assertEqual(settings.environment, "development")
        self.assertFalse(settings.debug)

    def test_health_endpoint_returns_expected_payload(self) -> None:
        client = TestClient(app)
        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(payload["environment"], get_settings().environment)
        self.assertEqual(payload["debug"], get_settings().debug)

    def test_db_health_endpoint_returns_connected_payload(self) -> None:
        class FakeResult:
            def scalar_one(self) -> int:
                return 1

        class FakeSession:
            def execute(self, *_args, **_kwargs) -> FakeResult:
                return FakeResult()

            def close(self) -> None:
                return None

        def override_get_db():
            yield FakeSession()

        app.dependency_overrides[get_db] = override_get_db
        client = TestClient(app)
        response = client.get("/health/db")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy", "database": "connected"})


if __name__ == "__main__":
    unittest.main()
