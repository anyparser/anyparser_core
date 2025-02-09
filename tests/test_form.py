import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core import OcrLanguage, OCRPreset
from anyparser_core.form import build_form
from anyparser_core.options import AnyparserParsedOption, UploadedFile


@pytest.fixture
def sample_file():
    return UploadedFile(filename="test.txt", contents=b"Hello, World!")


@pytest.fixture
def basic_parsed_option(sample_file):
    return AnyparserParsedOption(
        files=[sample_file],
        api_url="https://api.example.com",
        api_key="test_key",
        format="json",
        model="text",
        image=True,
        table=True,
    )


def test_build_form_basic(basic_parsed_option):
    """Test basic form building with minimal options"""
    boundary = "boundary123"
    form_data = build_form(basic_parsed_option, boundary)

    # Check if form_data is bytes
    assert isinstance(form_data, bytes)

    # Convert to string for easier testing
    form_str = form_data.decode("utf-8")

    # Check required fields
    assert "--boundary123" in form_str
    assert 'Content-Disposition: form-data; name="format"' in form_str
    assert 'Content-Disposition: form-data; name="model"' in form_str
    assert 'Content-Disposition: form-data; name="image"' in form_str
    assert 'Content-Disposition: form-data; name="table"' in form_str
    assert (
        'Content-Disposition: form-data; name="files"; filename="test.txt"' in form_str
    )
    assert "Hello, World!" in form_str


def test_build_form_with_ocr_options(basic_parsed_option):
    """Test form building with OCR options"""
    basic_parsed_option.model = "ocr"
    basic_parsed_option.ocr_language = [OcrLanguage.ENGLISH, OcrLanguage.SPANISH]
    basic_parsed_option.ocr_preset = OCRPreset.DOCUMENT

    boundary = "boundary123"
    form_data = build_form(basic_parsed_option, boundary)
    form_str = form_data.decode("utf-8")

    assert 'Content-Disposition: form-data; name="ocrLanguage"' in form_str
    assert "eng,spa" in form_str
    assert 'Content-Disposition: form-data; name="ocrPreset"' in form_str
    assert "document" in form_str


def test_build_form_multiple_files(basic_parsed_option):
    """Test form building with multiple files"""
    second_file = UploadedFile(filename="test2.pdf", contents=b"PDF content")
    basic_parsed_option.files.append(second_file)

    boundary = "boundary123"
    form_data = build_form(basic_parsed_option, boundary)
    form_str = form_data.decode("utf-8")

    assert 'filename="test.txt"' in form_str
    assert 'filename="test2.pdf"' in form_str
    assert "Hello, World!" in form_str
    assert "PDF content" in form_str


def test_build_form_content_type(basic_parsed_option):
    """Test content type detection for different file types"""
    pdf_file = UploadedFile(filename="test.pdf", contents=b"PDF content")
    basic_parsed_option.files = [pdf_file]

    boundary = "boundary123"
    form_data = build_form(basic_parsed_option, boundary)
    form_str = form_data.decode("utf-8")

    assert "Content-Type: application/pdf" in form_str


def test_build_form_basic():
    """Test basic form building."""
    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="text",
        files=[],
    )
    form_data = build_form(option, "boundary")
    assert b'name="format"' in form_data
    assert b'name="model"' in form_data


def test_build_form_with_image_table():
    """Test form building with image and table options."""
    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="text",
        image=True,
        table=False,
        files=[],
    )
    form_data = build_form(option, "boundary")
    assert b'name="image"' in form_data
    assert b'name="table"' in form_data


def test_build_form_ocr():
    """Test form building with OCR options."""
    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="ocr",
        ocr_language=[OcrLanguage.JAPANESE],
        ocr_preset=OCRPreset.SCAN,
        files=[],
    )
    form_data = build_form(option, "boundary")
    assert b'name="ocrLanguage"' in form_data
    assert b'name="ocrPreset"' in form_data


def test_build_form_crawler():
    """Test form building with crawler options."""
    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="crawler",
        url="https://example.com",
        max_depth=2,
        max_executions=10,
        strategy="LIFO",
        traversal_scope="subtree",
    )
    form_data = build_form(option, "boundary")
    assert b'name="url"' in form_data
    assert b'name="maxDepth"' in form_data
    assert b'name="maxExecutions"' in form_data
    assert b'name="strategy"' in form_data
    assert b'name="traversalScope"' in form_data


def test_build_form_with_files(tmp_path):
    """Test form building with file uploads."""
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(b"test content")

    from anyparser_core.options import UploadedFile

    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="text",
        files=[UploadedFile(filename="test.txt", contents=b"test content")],
    )
    form_data = build_form(option, "boundary")
    assert b'name="files"' in form_data
    assert b'filename="test.txt"' in form_data
    assert b"Content-Type: text/plain" in form_data
    assert b"test content" in form_data


def test_build_form_unknown_mime_type(tmp_path):
    """Test form building with unknown file type."""
    from anyparser_core.options import UploadedFile

    option = AnyparserParsedOption(
        api_url="https://api.example.com",
        api_key="test-key",
        format="json",
        model="text",
        files=[UploadedFile(filename="test.unknown", contents=b"test content")],
    )
    form_data = build_form(option, "boundary")
    assert b"Content-Type: application/octet-stream" in form_data
