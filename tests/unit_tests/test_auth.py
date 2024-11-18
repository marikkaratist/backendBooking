from src.services.auth import AuthService


def test_create_access_token():
    data = {"user_1": 1}
    jwt = AuthService().create_access_token(data)

    assert jwt
    assert isinstance(jwt, str)
