"""
Validation module for options
"""

from ..config.hardcoded import OCR_LANGUAGES, OCR_PRESETS
from ..options import AnyparserParsedOption


def validate_option(parsed: AnyparserParsedOption) -> None:
    """
    Validates parsing options configuration

    Raises:
        ValueError: If validation fails
    """
    if not parsed.get("api_url"):
        raise ValueError("API URL is required")

    if ocr_language := parsed.get("ocr_language"):
        for language in ocr_language:
            if language.value not in OCR_LANGUAGES:
                raise ValueError(f'Invalid OCR language: "{language.value}"')

    if ocr_preset := parsed.get("ocr_preset"):
        if ocr_preset.value not in OCR_PRESETS:
            raise ValueError(f'Invalid OCR preset: "{ocr_preset.value}"')
