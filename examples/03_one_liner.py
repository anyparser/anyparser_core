import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core import Anyparser

multiple_files = ["docs/sample.docx", "docs/sample.pdf"]

result = asyncio.run(Anyparser().parse(multiple_files))

for item in result:
    print("-" * 100)
    print("File:", item.original_filename)
    print("Checksum:", item.checksum)
    print("Total characters:", item.total_characters)
    print("Markdown:", item.markdown)

print("-" * 100)
