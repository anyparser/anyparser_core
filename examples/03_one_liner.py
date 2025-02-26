import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ------------------------------------------------------------------------------

from anyparser_core import Anyparser

print(asyncio.run(Anyparser().parse(["docs/sample.docx", "docs/sample.pdf"])))

