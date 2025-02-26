# Anyparser Core: Your Foundation for AI Data Preparation

https://anyparser.com

**Unlock the potential of your AI models with Anyparser Core, the Python SDK designed for high-performance content extraction and format conversion.**  Built for developers, this SDK streamlines the process of acquiring clean, structured data from diverse sources, making it an indispensable tool for building cutting-edge applications in **Retrieval Augmented Generation (RAG)**, **Agentic AI**, **Generative AI**, and robust **ETL Pipelines**.

**Key Benefits for AI Developers:**

* **Rapid Data Acquisition for RAG:** Extract information up to 10x faster than traditional methods, accelerating the creation of your knowledge bases for efficient RAG implementations.
* **High-Accuracy Data for Generative AI:** Achieve up to 10x improvement in extraction accuracy, ensuring your Generative AI models are trained and operate on reliable, high-quality data. Output in JSON or Markdown is directly consumable by AI processes.
* **Cost-Effective Knowledge Base Construction:**  Efficiently build and maintain knowledge bases from unstructured data, significantly reducing the overhead for RAG, Agentic AI, and other AI applications.
* **Developer-First Design:** Unlimited local usage (fair use policies apply) allows for rapid experimentation and seamless integration into your existing AI workflows.
* **Optimized for ETL Pipelines:**  Provides a robust extraction layer for your ETL processes, handling a wide variety of file types and URLs to feed your data lakes and AI systems.

**Get Started Quickly:**

1. **Free Access:** Obtain your API credentials and start building your AI data pipelines today at [Anyparser Studio](https://studio.anyparser.com/).
2. **Installation:** Install the SDK with a simple pip command.
3. **Run Examples:**  Copy and paste the provided examples to see how easy it is to extract data for your AI projects.

Before starting, add a new API key on the [Anyparser Studio](https://studio.anyparser.com/).


```bash
export ANYPARSER_API_URL=https://anyparserapi.com
export ANYPARSER_API_KEY=<your-api-key>
```

or

```bash
export ANYPARSER_API_URL=https://eu.anyparserapi.com
export ANYPARSER_API_KEY=<your-api-key>
```

## Installation

```bash
pip install anyparser-core
```

## Core Usage Examples for AI Applications

These examples demonstrate how to use `Anyparser Core` for common AI tasks, arranged from basic to advanced usage.


### Example 1: Quick Start with Single Document

When you're just getting started or prototyping, you can use this simplified approach with minimal configuration:

```python
import os
import asyncio

from anyparser_core import Anyparser

single_file = "docs/sample.docx"

# Instantiate with default settings, assuming API credentials are
# set as environment variables.
parser = Anyparser()

result = asyncio.run(parser.parse(single_file))
print(result)
```

### Example 2: Building a RAG Knowledge Base from Local Documents

This example showcases how to extract structured data from local files with full configuration, preparing them for indexing in a RAG system. The JSON output is ideal for vector databases and downstream AI processing. Perfect for building your initial knowledge base with high-quality, structured data.

```python
import os
import asyncio
import sys

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
```

### Example 3: OCR Processing for Image-Based Documents

Extract text from images and scanned documents using our advanced OCR capabilities. This example shows how to configure language and preset options for optimal results, particularly useful for processing historical documents, receipts, or any image-based content:

```python
import os
import asyncio
import sys

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
```

### Example 4: Processing Multiple Documents for Batch RAG Updates

This example demonstrates how to process multiple documents in a single batch, ideal for updating your RAG knowledge base or processing document collections efficiently:

```python
import os
import asyncio
import sys

from anyparser_core import Anyparser, AnyparserOption

multiple_files = ["docs/sample.docx", "docs/sample.pdf"]

options = AnyparserOption(
    api_url=os.getenv("ANYPARSER_API_URL"),
    api_key=os.getenv("ANYPARSER_API_KEY"),
    format="json",
    image=True,
    table=True,
)

parser = Anyparser(options)

result = asyncio.run(parser.parse(multiple_files))

for item in result:
    print("-" * 100)
    print("File:", item.original_filename)
    print("Checksum:", item.checksum)
    print("Total characters:", item.total_characters)
    print("Markdown:", item.markdown)

print("-" * 100)
```

### Example 5: Web Crawling for Dynamic Knowledge Base Updates

Keep your knowledge base fresh with our powerful web crawling capabilities. This example shows how to crawl websites while respecting robots.txt directives and maintaining politeness delays:

```python
import os
import asyncio
import sys

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

for candidate in result:
    print("Start URL            :", candidate.start_url)
    print("Total characters     :", candidate.total_characters)
    print("Total items          :", candidate.total_items)
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
```

## Configuration for Optimized AI Workloads

The `Anyparser` class utilizes the `AnyparserOption` dataclass for flexible configuration, allowing you to fine-tune the extraction process for different AI use cases.

```python
from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from anyparser_core import OcrLanguage, OcrPreset

@dataclass
class AnyparserOption:
    """Configuration options for the Anyparser API."""
    
    # API Configuration
    api_url: Optional[str] = None  # API endpoint URL, defaults to environment variable ANYPARSER_API_URL
    api_key: Optional[str] = None  # API key, defaults to environment variable ANYPARSER_API_KEY
    
    # Output Format
    format: Literal["json", "markdown", "html"] = "json"  # Output format
    
    # Processing Model
    model: Literal["text", "ocr", "vlm", "lam", "crawler"] = "text"  # Processing model to use
    
    # Text Processing
    encoding: Literal["utf-8", "latin1"] = "utf-8"  # Text encoding
    
    # Content Extraction
    image: Optional[bool] = None  # Enable/disable image extraction
    table: Optional[bool] = None  # Enable/disable table extraction
    
    # Input Sources
    files: Optional[Union[str, List[str]]] = None  # Input files to process
    url: Optional[str] = None  # URL for crawler model
    
    # OCR Configuration
    ocr_language: Optional[List[OcrLanguage]] = None  # Languages for OCR processing
    ocr_preset: Optional[OcrPreset] = None  # Preset configuration for OCR
    
    # Crawler Configuration
    max_depth: Optional[int] = None  # Maximum crawl depth
    max_executions: Optional[int] = None  # Maximum number of pages to crawl
    strategy: Optional[Literal["LIFO", "FIFO"]] = None  # Crawling strategy
    traversal_scope: Optional[Literal["subtree", "domain"]] = None  # Crawling scope
```

**Key Configuration Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_url` | `Optional[str]` | `None` | API endpoint URL. Defaults to `ANYPARSER_API_URL` environment variable |
| `api_key` | `Optional[str]` | `None` | API key for authentication. Defaults to `ANYPARSER_API_KEY` environment variable |
| `format` | `str` | `"json"` | Output format: `"json"`, `"markdown"`, or `"html"` |
| `model` | `str` | `"text"` | Processing model: `"text"`, `"ocr"`, `"vlm"`, `"lam"`, or `"crawler"` |
| `encoding` | `str` | `"utf-8"` | Text encoding: `"utf-8"` or `"latin1"` |
| `image` | `Optional[bool]` | `None` | Enable/disable image extraction |
| `table` | `Optional[bool]` | `None` | Enable/disable table extraction |
| `files` | `Optional[Union[str, List[str]]]` | `None` | Input files to process |
| `url` | `Optional[str]` | `None` | URL for crawler model |
| `ocr_language` | `Optional[List[OcrLanguage]]` | `None` | Languages for OCR processing |
| `ocr_preset` | `Optional[OcrPreset]` | `None` | Preset configuration for OCR |
| `max_depth` | `Optional[int]` | `None` | Maximum crawl depth for crawler model |
| `max_executions` | `Optional[int]` | `None` | Maximum number of pages to crawl |
| `strategy` | `Optional[str]` | `None` | Crawling strategy: `"LIFO"` or `"FIFO"` |
| `traversal_scope` | `Optional[str]` | `None` | Crawling scope: `"subtree"` or `"domain"` |

**OCR Presets:**

The following OCR presets are available for optimized document processing:

- `OcrPreset.DOCUMENT` - General document processing
- `OcrPreset.HANDWRITING` - Handwritten text recognition
- `OcrPreset.SCAN` - Scanned document processing
- `OcrPreset.RECEIPT` - Receipt processing
- `OcrPreset.MAGAZINE` - Magazine/article processing
- `OcrPreset.INVOICE` - Invoice processing
- `OcrPreset.BUSINESS_CARD` - Business card processing
- `OcrPreset.PASSPORT` - Passport document processing
- `OcrPreset.DRIVER_LICENSE` - Driver's license processing
- `OcrPreset.IDENTITY_CARD` - ID card processing
- `OcrPreset.LICENSE_PLATE` - License plate recognition
- `OcrPreset.MEDICAL_REPORT` - Medical document processing
- `OcrPreset.BANK_STATEMENT` - Bank statement processing

**Model Types for AI Data Pipelines:**

Select the appropriate processing model based on your AI application needs:

* `'text'`:  Optimized for extracting textual content for language models and general text-based RAG.
* `'ocr'`:  Performs Optical Character Recognition to extract text from image-based documents, expanding your data sources for AI training and knowledge bases. **Essential for processing scanned documents for RAG and Generative AI.**
* `'vlm'`:  Utilizes a Vision-Language Model for advanced understanding of image content, enabling richer context for Generative AI and more sophisticated Agentic AI perception.
* `'lam'` (Coming Soon): Employs a Large-Audio Model for extracting insights from audio data, opening new possibilities for multimodal AI applications.
* `'crawler'`: Enables website crawling to gather up-to-date information for dynamic AI knowledge bases and Agentic AI agents.

**OCR Configuration for Enhanced AI Data Quality (when `model='ocr'`):**

Fine-tune OCR settings for optimal accuracy when processing image-based documents. This is critical for ensuring high-quality data for your AI models.

| Option         | Type              | Default | Description                                                                                                 | Relevance for AI                                                                             |
|----------------|-------------------|---------|-------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `ocr_language` | `Optional[List[str]]` | `None`  | List of ISO 639-2 language codes for OCR, ensuring accurate text extraction for multilingual documents.      | **Essential for accurate data extraction from documents in different languages for global AI.** |
| `ocr_preset`   | `Optional[str]`   | `None`  | Predefined configuration for specific document types to optimize OCR accuracy.                               | **Use presets to improve accuracy for specific document types used in your AI workflows.**    |

**Available OCR Presets for AI Data Preparation:**

Leverage these presets for common document types used in AI datasets:

* `'document'`:  General-purpose OCR for standard documents.
* `'handwriting'`: Optimized for handwritten text, useful for digitizing historical documents or notes for AI analysis.
* `'scan'`:  For scanned documents and images.
* **Specific Document Presets (valuable for structured data extraction):** `'receipt'`, `'magazine'`, `'invoice'`, `'business-card'`, `'passport'`, `'driver-license'`, `'identity-card'`, `'license-plate'`, `'medical-report'`, `'bank-statement'`. **These presets are crucial for building structured datasets for training specialized AI models or powering Agentic AI agents that interact with these document types.**


## Contributing to AI-Ready Data Extraction

We welcome contributions to the `Anyparser Core` SDK, particularly those that enhance its capabilities for AI data preparation. Please refer to the [Contribution Guidelines](CONTRIBUTING.md).

# Frequently Asked Questions (FAQ)

1. **Do I have to buy a license to use the SDK?**
    - No, there's no need to buy a license to use the SDK. You can get started right away.
2. **Do you store my documents?**
    - No, we do not store any of your documents. All data is processed in real-time and discarded after the task is completed.
3. **Is there a way to test the software or have a free trial?**
    - You don't need to commit. You can use the API on your developer machine for free with a fair usage policy. OCR and VLM models are not free, but you can purchase a tiny (as low as $5) credit to test the quality of the output.
4. **Can I get a refund?**
    - No, we do not offer any refunds.
5. **Is Anyparser Available in My Region?**
    - Currently, Anyparser is only available in the EU, US, and a few other countries. We are working on expanding to more regions.
6. **Why don't you have paid plans?**
    - We use a pay-per-use model to offer [flexible pricing](https://anyparser.com/pricing) and avoid locking customers into expensive subscriptions.
7. **Does the license allow me to use the software in a SaaS product?**
    - Yes, the license permits usage in SaaS products.
8. **What kind of support will I get?**
    - We offer email and ticket-based support.
9. **Does the SDK support chunking and embedding?**
    - No, our service focuses on the extraction layer in your ETL pipeline. Chunking and embedding would be handled separately by your own system.
10. **Does the SDK support multiple file uploads?**
    - Yes.
11. **Does it support converting receipts to structured output?**
    - Yes, Anyparser can extract data from receipts and convert it into structured formats.
12. **Does it support multiple languages?**
    - Yes, Anyparser supports multiple languages for text extraction.
13. **Where are your servers located?**
    - Our servers are located in the US with a federated setup across United States, Europe, and Asia. We are adding more regions as we move forward.

### Why Use Anyparser SDKs?

- **100% Free for Developers**: As long as you're running Anyparser on your local laptop or personal machine (not on servers), unlimited extraction is completely free under our fair usage policy. There’s no need to pay for anything, making it perfect for developers testing and building on their development environment.
- **Speed**: Up to 10x faster than traditional parsing tools, with optimized processing for both small and large documents.
- **Accuracy**: Get highly accurate, structured outputs even from complex formats like OCR, tables, and charts.
- **Scalability**: Whether you're processing a few documents or millions, our SDKs ensure smooth integration with your workflows.
- **Multiple File Support**: Effortlessly parse bulk files, saving time and optimizing batch processing.
- **Zero Learning Curve**: The SDKs come with comprehensive examples, documentation, and minimal setup, allowing you to get started immediately without needing deep technical expertise.

# Product Roadmap

While Anyparser is already a powerful solution for document parsing, we’re committed to continually improving and expanding our platform. Our roadmap includes:

- **Further Integrations**: We plan to add more integrations with industry-standard tools and platforms, enabling deeper workflows and expanding compatibility.
- **Additional Models**: We aim to introduce new parsing models to handle more complex or specialized data extraction tasks.
- **Enhanced Features**: Continuous improvement of our existing features, such as support for additional file formats, optimization of processing speed, and improved accuracy.


## License

Apache-2.0

## Support for AI Developers

For technical support or inquiries related to using Anyparser Core for AI applications, please visit our [Community Discussions](https://github.com/anyparser/anyparser_core/discussions). We are here to help you build the next generation of AI applications.

