import pytest
from receiver.service import controller
from receiver.service.decrypter import Decrypter


@pytest.fixture
def client():
    """
    pytest fixture for cresting app client.
    :return:
    """
    return controller.app.test_client()


@pytest.fixture
def set_mock_decrypty(monkeypatch):
    """pytest mock decrypt method in Decrypt class"""
    def fake_decrypt_method(self, testfiledata, testfilelocation):
        pass
    monkeypatch.setattr(Decrypter, "decrypt", fake_decrypt_method)
