import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core import Anyparser, AnyparserOption, OcrLanguage, OcrPreset

single_file = "docs/document.png"

options = AnyparserOption(
    api_url=os.getenv("ANYPARSER_API_URL"),
    api_key=os.getenv("ANYPARSER_API_KEY"),
    model="ocr",
    format="markdown",
    ocr_language=[OcrLanguage.JAPANESE],
    ocr_preset=OcrPreset.SCAN,
)

parser = Anyparser(options)

result = asyncio.run(parser.parse(single_file))

print(result)
