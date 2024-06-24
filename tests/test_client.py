import os
import time

from koemotion import Koemotion


def test_api_key_from_env():
    client = Koemotion()
    assert client.api_key == os.environ.get("KOEMOTION_API_KEY")


def test_api_key_from_arg():
    client = Koemotion(api_key="dummy")
    assert client.api_key == "dummy"


def test_base_url_from_env():
    client = Koemotion()
    assert client.base_url == os.environ.get("KOEMOTION_BASE_URL")


def test_base_url_from_arg():
    client = Koemotion(base_url="https://example.com")
    assert client.base_url == "https://example.com"


def test_request():
    client = Koemotion()
    response = client.request({"text": "こんにちは、世界"})
    assert response.response.status_code == 200
    assert "audio" in response.response.json()
    time.sleep(1)


def test_request_stream():
    client = Koemotion()
    response = client.request(
        {"text": "こんにちは、世界", "output_format": "wav", "streaming": True}
    )
    assert response.response.status_code == 200
    assert response.response.content[:4] == b"RIFF"
    time.sleep(1)
