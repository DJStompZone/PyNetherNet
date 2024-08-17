import pytest
from pytest_mock import MockerFixture
from pynethernet.playfab_client import PlayFabClient


@pytest.fixture
def playfab_client():
    return PlayFabClient()


def test_playfab_client_init(playfab_client):
    assert playfab_client.TITLE_ID == "20CA2"
    assert playfab_client.TITLE_SHARED_SECRET == "S8RS53ZEIGMYTYG856U3U19AORWXQXF41J7FT3X9YCWAC7I35X"


def test_playfab_client_load_settings(mocker: MockerFixture, playfab_client):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('builtins.open', mocker.mock_open(read_data='{"key": "value"}'))
    settings = playfab_client.load_settings()
    assert settings == {"key": "value"}


def test_playfab_client_save_settings(mocker: MockerFixture, playfab_client):
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    playfab_client.playfab_settings = {"key": "value"}
    playfab_client.save_settings()
    mock_open.assert_called_once_with("settings.json", 'w')


def test_playfab_client_send_playfab_request(mocker: MockerFixture, playfab_client):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"key": "value"}}
    mocker.patch('requests.Session.post', return_value=mock_response)
    response = playfab_client.send_playfab_request("/test", {})
    assert response == {"key": "value"}
