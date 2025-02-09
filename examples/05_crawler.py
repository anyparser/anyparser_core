import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core import Anyparser, AnyparserOption

item = "https://anyparser.com"

options = AnyparserOption(
    api_url=os.getenv("ANYPARSER_API_URL"),
    api_key=os.getenv("ANYPARSER_API_KEY"),
    model="crawler",
    format="json",
    max_depth=50,
    max_executions=2,
    strategy="LIFO",
    traversal_scope="subtree",
)

parser = Anyparser(options)

result = asyncio.run(parser.parse(item))
print("\n")

for candidate in result:
    print("Start URL            :", candidate.start_url)
    print("Total characters     :", candidate.total_characters)
    print("Total items          :", candidate.total_items)
    # print("Markdown           :", candidate.markdown)
    print("Robots directive     :", candidate.robots_directive)
    print("\n")
    print("*" * 100)
    print("Begin Crawl")
    print("*" * 100)
    print("\n")

    for item in candidate.items:
        if candidate.items.index(item) > 0:
            print("-" * 100)
            print("\n")

        print("URL                  :", item.url)
        print("Title                :", item.title)
        print("Status message       :", item.status_message)
        print("Total characters     :", item.total_characters)
        print("Politeness delay     :", item.politeness_delay)
        print("Content:\n")
        print(item.markdown)

    print("*" * 100)
    print("End Crawl")
    print("*" * 100)
    print("\n")
