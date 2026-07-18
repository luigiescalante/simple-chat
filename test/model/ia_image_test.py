import base64
import uuid
from unittest import mock

import pytest

from app.model.ai_image import IaImage


@pytest.fixture
def valid_env(monkeypatch):
    monkeypatch.setenv("OPENIA_IMAGE_MODEL", "fake-model")


@pytest.fixture
def ia_image(valid_env):
    return IaImage(
        prompt="generic image",
        quality="standard",
        size="1024x1024",
    )


def test_new_ia_image_success(valid_env):
    result = IaImage(
        prompt="generic image",
        quality="standard",
        size="1024x1024",
    )
    assert result.ia_model == "fake-model"


def test_new_ia_image_failure_missing_env(monkeypatch):
    monkeypatch.delenv("OPENIA_IMAGE_MODEL", raising=False)
    with pytest.raises(ValueError, match="invalid image ia_model"):
        IaImage(
            prompt="generic image",
            quality="standard",
            size="1024x1024",
        )


def test_new_ia_image_failure_empty_env(monkeypatch):
    monkeypatch.setenv("OPENIA_IMAGE_MODEL", "")
    with pytest.raises(ValueError, match="invalid image ia_model"):
        IaImage(
            prompt="generic image",
            quality="standard",
            size="1024x1024",
        )


def test_save_image_success(ia_image):
    image_bytes = b"fake image binary content"
    image_b64 = base64.b64encode(image_bytes).decode()
    with mock.patch("builtins.open", mock.mock_open()) as mocked_open:
        result_id = ia_image.save_image(image_b64)
        assert isinstance(result_id, uuid.UUID)
        assert result_id == ia_image.id
        mocked_open.return_value.write.assert_called_once_with(image_bytes)


def test_save_image_invalid_base64_raises_binascii_error(ia_image):
    with pytest.raises(ValueError):
        ia_image.save_image("not-valid-base64!!!")


def test_save_image_file_not_found_error(ia_image):
    image_b64 = base64.b64encode(b"fake image binary content").decode()
    with mock.patch("builtins.open", side_effect=FileNotFoundError("missing dir")):
        with pytest.raises(FileNotFoundError):
            ia_image.save_image(image_b64)


def test_save_image_permission_error(ia_image):
    image_b64 = base64.b64encode(b"fake image binary content").decode()
    with mock.patch("builtins.open", side_effect=PermissionError("denied")):
        with pytest.raises(PermissionError):
            ia_image.save_image(image_b64)


def test_save_image_os_error(ia_image):
    image_b64 = base64.b64encode(b"fake image binary content").decode()
    with mock.patch("builtins.open", side_effect=OSError("disk full")):
        with pytest.raises(OSError):
            ia_image.save_image(image_b64)


def test_save_image_unexpected_error(ia_image):
    image_b64 = base64.b64encode(b"fake image binary content").decode()
    with mock.patch("builtins.open", side_effect=RuntimeError("boom")):
        with pytest.raises(RuntimeError):
            ia_image.save_image(image_b64)