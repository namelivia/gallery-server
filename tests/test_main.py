from mock import patch, Mock
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
from freezegun import freeze_time


@freeze_time("2013-04-09")
class TestApp:
    @patch("app.users.api.UserInfo.get_current")
    def test_get_current_user(self, m_get_user_info, client):
        m_get_user_info.return_value = {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
            "name": "User Name",
        }
        response = client.get(
            "/users/me", headers={"X-Pomerium-Jwt-Assertion": "jwt_assertion"}
        )
        assert response.status_code == 200
        assert response.json() == {
            "aud": ["example"],
            "email": "user@example.com",
            "exp": 1237658,
            "iat": 1237658,
            "iss": "test.example.com",
            "nbf": 1237658,
            "sub": "user",
            "name": "User Name",
        }
        m_get_user_info.assert_called_with("jwt_assertion")

    def test_get_all_images(self, client, database_test_session):
        response = client.get("/images")
        assert response.status_code == 200
        assert response.json() == [{"url": "http://foo.bar"}]
