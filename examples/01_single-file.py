import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core import Anyparser, AnyparserOption

single_file = "docs/sample.docx"

options = AnyparserOption(
    api_url=os.getenv("ANYPARSER_API_URL"),
    api_key=os.getenv("ANYPARSER_API_KEY"),
    format="json",
    image=True,
    table=True,
)

parser = Anyparser(options)

result = asyncio.run(parser.parse(single_file))

for item in result:
    print("-" * 100)
    print("File:", item.original_filename)
    print("Checksum:", item.checksum)
    print("Total characters:", item.total_characters)
    print("Markdown:", item.markdown)

print("-" * 100)
