import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core.config.hardcoded import OcrLanguage, OcrPreset
from anyparser_core.validator.option import validate_option


def test_validate_option_missing_api_url():
    """Test validation with missing API URL"""
    with pytest.raises(ValueError, match="API URL is required"):
        validate_option({"api_url": None})


def test_validate_option_invalid_ocr_language():
    """Test validation with invalid OCR language"""
    invalid_language = type("InvalidLanguage", (), {"value": "invalid"})()

    with pytest.raises(ValueError, match='Invalid OCR language: "invalid"'):
        validate_option(
            {"api_url": "https://api.example.com", "ocr_language": [invalid_language]}
        )


def test_validate_option_invalid_ocr_preset():
    """Test validation with invalid OCR preset"""
    invalid_preset = type("InvalidPreset", (), {"value": "invalid"})()

    with pytest.raises(ValueError, match='Invalid OCR preset: "invalid"'):
        validate_option(
            {"api_url": "https://api.example.com", "ocr_preset": invalid_preset}
        )


def test_validate_option_valid_options():
    """Test validation with valid options"""
    options = {
        "api_url": "https://api.example.com",
        "api_key": "test-key",
        "ocr_language": [OcrLanguage.ENGLISH, OcrLanguage.SPANISH],
        "ocr_preset": OcrPreset.DOCUMENT,
    }

    # Should not raise any exceptions
    validate_option(options)


def test_validate_option_no_ocr_options():
    """Test validation without OCR options"""
    options = {"api_url": "https://api.example.com", "api_key": "test-key"}

    # Should not raise any exceptions
    validate_option(options)
