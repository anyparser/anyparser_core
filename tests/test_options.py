import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core.config.hardcoded import OcrLanguage, OCRPreset
from anyparser_core.options import (
    AnyparserOption,
    AnyparserParsedOption,
    UploadedFile,
    build_options,
)
from anyparser_core.validator import validate_option


@pytest.fixture
def mock_api_key():
    return "test-api-key-12345"


def test_build_options_defaults(monkeypatch, mock_api_key):
    """Test building options with defaults"""
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    options = build_options()
    assert isinstance(options, dict)
    assert options["api_url"] == os.getenv(
        "ANYPARSER_API_URL", "https://anyparserapi.com"
    )
    assert options["api_key"] == mock_api_key
    assert options["format"] == "json"
    assert options["model"] == "text"
    assert options["image"] is True
    assert options["table"] is True
    assert options["ocr_language"] is None
    assert options["ocr_preset"] is None


def test_build_options_with_env_vars(monkeypatch):
    """Test building options with environment variables"""
    test_api_url = "https://test-api.example.com"
    test_api_key = "test-key-123"

    monkeypatch.setenv("ANYPARSER_API_URL", test_api_url)
    monkeypatch.setenv("ANYPARSER_API_KEY", test_api_key)

    options = build_options()
    assert options["api_url"] == test_api_url
    assert options["api_key"] == test_api_key


def test_build_options_with_custom_options(mock_api_key, monkeypatch):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test building options with custom values"""
    custom_options = AnyparserOption(
        api_url="https://custom.example.com",
        api_key=mock_api_key,
        format="markdown",
        model="ocr",
        image=False,
        table=False,
        ocr_language=[OcrLanguage.ENGLISH],
        ocr_preset=OCRPreset.DOCUMENT,
    )

    options = build_options(custom_options)
    assert options["api_url"] == "https://custom.example.com"
    assert options["api_key"] == mock_api_key
    assert options["format"] == "markdown"
    assert options["model"] == "ocr"
    assert options["image"] is False
    assert options["table"] is False
    assert options["ocr_language"] == [OcrLanguage.ENGLISH]
    assert options["ocr_preset"] == OCRPreset.DOCUMENT


def test_anyparser_parsed_file():
    """Test AnyparserPdfPage dataclass"""
    file = UploadedFile(filename="test.txt", contents=b"test content")
    assert file.filename == "test.txt"
    assert file.contents == b"test content"


def test_anyparser_parsed_option():
    """Test AnyparserParsedOption dataclass"""
    file = UploadedFile(filename="test.txt", contents=b"test content")
    parsed_option = AnyparserParsedOption(
        files=[file],
        api_url="https://api.example.com",
        api_key="test-key",
        format="html",
        model="text",
        image=False,
        table=True,
        ocr_language=[OcrLanguage.ENGLISH],
        ocr_preset=OCRPreset.HANDWRITING,
    )

    assert len(parsed_option.files) == 1
    assert parsed_option.api_url == "https://api.example.com"
    assert parsed_option.api_key == "test-key"
    assert parsed_option.format == "html"
    assert parsed_option.model == "text"
    assert parsed_option.image is False
    assert parsed_option.table is True
    assert parsed_option.ocr_language == [OcrLanguage.ENGLISH]
    assert parsed_option.ocr_preset == OCRPreset.HANDWRITING


def test_anyparser_option_validation():
    """Test validation of AnyparserOption fields"""
    # Test invalid OCR language
    with pytest.raises(ValueError):
        options = build_options(AnyparserOption(ocr_language=[OcrLanguage("invalid")]))
        validate_option(options)

    # Test invalid OCR preset
    with pytest.raises(ValueError):
        options = build_options(AnyparserOption(ocr_preset=OCRPreset("invalid")))
        validate_option(options)

    # Test missing API URL
    with pytest.raises(ValueError):
        options = build_options(AnyparserOption(api_url=None))
        validate_option(options)


def test_api_key_validation_non_string():
    """Test API key validation with non-string input"""
    from anyparser_core.options import validate_api_key

    non_string_values = [None, 123, True, [], {}, 1.23]
    for value in non_string_values:
        with pytest.raises(ValueError, match="Invalid API key format"):
            validate_api_key(value)


def test_api_key_validation_empty():
    """Test API key validation with empty string"""
    from anyparser_core.options import validate_api_key

    with pytest.raises(ValueError, match="API key is required but not provided"):
        validate_api_key("")


def test_invalid_api_url(monkeypatch):
    """Test validation of invalid API URL"""
    monkeypatch.setenv("ANYPARSER_API_URL", "not-a-url")
    with pytest.raises(ValueError, match="Invalid API URL"):
        build_options()


def test_file_lock_errors():
    """Test file locking error conditions"""
    import os
    import tempfile

    from anyparser_core.validator.main import file_lock

    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        with file_lock("/nonexistent/file"):
            pass

    # Test file locked by another process
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"test")
        tf.flush()

        with open(tf.name, "rb") as f1:
            # Lock the file
            import fcntl

            fcntl.flock(f1.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Try to lock it again
            with pytest.raises(IOError):
                with file_lock(tf.name):
                    pass

            # Release the lock
            fcntl.flock(f1.fileno(), fcntl.LOCK_UN)

        os.unlink(tf.name)
