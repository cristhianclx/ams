# -*- coding: utf-8 -*-

# mypy: disable-error-code=attr-defined
# pylint:disable=no-member

from collections import Counter
from datetime import timedelta
from json import dumps
from string import ascii_uppercase
from typing import Callable
from unittest.mock import MagicMock

from faker import Factory
from fastapi.testclient import TestClient
from models.stock import Stock
from models.user import User
from pytest import MonkeyPatch
from pytest import fixture as pytest__fixture
from requests_mock import Mocker
from sqlalchemy.orm import Session
from tests.base import _client  # noqa:F401 pylint:disable=unused-import
from tests.base import session  # noqa:F401 pylint:disable=unused-import
from tests.services.v1 import URL_API_V1
from tests.services.v1.test_users import _user  # noqa:F401 pylint:disable=unused-import
from tests.services.v1.test_users import URL_API_V1_USERS
from utils import auth
from utils.alpha_vantage import ALPHA_VANTAGE_URL
from utils.auth import create_access_token

URL_API_V1_STOCKS: str = f"{URL_API_V1}/stocks"

faker = Factory.create()


@pytest__fixture
def _stock(session: Session) -> Callable[[], Stock]:  # pylint:disable=redefined-outer-name
    def __stock() -> Stock:
        item = Stock(
            code=faker.bothify(text="????", letters=ascii_uppercase),
            name=faker.name(),
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    return __stock


class TestStockService:
    def test_get_without_credentials(self, _client: TestClient, _stock: Stock) -> None:
        response = _client.get(f"{URL_API_V1_STOCKS}/{_stock().code}/")
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Not authenticated"

    def test_get_with_wrong_credentials(self, _client: TestClient, _stock: Stock) -> None:
        response = _client.get(
            f"{URL_API_V1_STOCKS}/{_stock().code}/",
            headers={
                "Authorization": "Bearer JWT",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Could not decode credentials"

    def test_get_with_expired_credentials(self, _client: TestClient, _stock: Stock, _user: User) -> None:
        token = create_access_token(
            data={
                "sub": _user().email,
            },
            expires_delta=-timedelta(minutes=15),
        )
        response = _client.get(
            f"{URL_API_V1_STOCKS}/{_stock().code}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Could not decode credentials"

    def test_get_not_found(self, _client: TestClient, _user: User, monkeypatch: MonkeyPatch) -> None:
        user = _user()
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.get(
            f"{URL_API_V1_STOCKS}/ABCED/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 404

    def test_get_with_service_down(
        self,
        _client: TestClient,
        _stock: Stock,
        _user: User,
        monkeypatch: MonkeyPatch,
        requests_mock: Mocker,
    ) -> None:
        stock = _stock()
        requests_mock.get(
            ALPHA_VANTAGE_URL,
            status_code=503,
        )
        user = _user()
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        response = _client.post(
            f"{URL_API_V1_USERS}/login/",
            json={
                "email": user.email,
                "password": "123456",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "login" in data
        assert "token" in data["login"]
        token = data["login"]["token"]
        response = _client.get(
            f"{URL_API_V1_STOCKS}/{stock.code}/",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 503

    def test_get_with_different_keys(
        self,
        _client: TestClient,
        _stock: Stock,
        _user: User,
        monkeypatch: MonkeyPatch,
        requests_mock: Mocker,
    ) -> None:
        stock = _stock()
        requests_mock.get(
            ALPHA_VANTAGE_URL,
            text=dumps(
                {
                    "Time Series (Daily)": {
                        "2023-01-10": {
                            "1. open": "130.96",
                            "2. high": "133.8494",
                            "3. low": "130.34",
                            "4. close": "132.89",
                        },
                        "2023-01-09": {
                            "1. open": "127.27",
                            "2. high": "133.44",
                            "3. low": "127.15",
                            "4. close": "132.99",
                        },
                    }
                }
            ),
        )
        # we can try to get some api keys to test cache
        for iterator in range(1, 10):  # pylint:disable=unused-variable
            user = _user()
            monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
            response = _client.post(
                f"{URL_API_V1_USERS}/login/",
                json={
                    "email": user.email,
                    "password": "123456",
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert "login" in data
            assert "token" in data["login"]
            token = data["login"]["token"]
            response = _client.get(
                f"{URL_API_V1_STOCKS}/{stock.code}/",
                headers={
                    "Authorization": f"Bearer {token}",
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert "code" in data
            assert data["code"] == stock.code
            assert data["name"] == stock.name
            assert data["price"] == {"high": 133.8494, "low": 130.34, "open": 130.96, "variation": -0.1}

    def test_get_with_same_key(
        self,
        _client: TestClient,
        _stock: Stock,
        _user: User,
        monkeypatch: MonkeyPatch,
        requests_mock: Mocker,
    ) -> None:
        stock = _stock()
        requests_mock.get(
            ALPHA_VANTAGE_URL,
            text=dumps(
                {
                    "Time Series (Daily)": {
                        "2023-01-10": {
                            "1. open": "130.96",
                            "2. high": "133.8494",
                            "3. low": "130.34",
                            "4. close": "132.89",
                        },
                        "2023-01-09": {
                            "1. open": "127.27",
                            "2. high": "133.44",
                            "3. low": "127.15",
                            "4. close": "132.99",
                        },
                    }
                }
            ),
        )
        user = _user()
        monkeypatch.setattr(auth, "get_user", MagicMock(return_value=user))
        # we can try to do some calls with same api key
        response_codes_raw = []
        for iterator in range(1, 100):  # pylint:disable=unused-variable
            response = _client.post(
                f"{URL_API_V1_USERS}/login/",
                json={
                    "email": user.email,
                    "password": "123456",
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert "login" in data
            assert "token" in data["login"]
            token = data["login"]["token"]
            response = _client.get(
                f"{URL_API_V1_STOCKS}/{stock.code}/",
                headers={
                    "Authorization": f"Bearer {token}",
                },
            )
            assert response.status_code in [200, 429]
            response_codes_raw.append(response.status_code)
        response_codes = Counter(response_codes_raw)
        assert response_codes[200] > 1
        assert response_codes[429] > 1
