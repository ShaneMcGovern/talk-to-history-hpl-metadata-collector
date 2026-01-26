# Talk to History: H.P. Lovecraft Brown Metadata Collector

[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)
<!-- [![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://github.com/astral-sh/uv)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: Public Domain](https://img.shields.io/badge/License-Public%20Domain-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/) -->

Automated metadata harvesting tool for H.P. Lovecraft's correspondence collection at Brown University's John Hay Library. Retrieves and saves structured metadata for public domain letters and manuscripts through the Brown Digital Repository API.

## Features

- **Targeted Collection Queries**: Searches specifically for Lovecraft's autograph letters, signed letters, and typed correspondence
- **Public Domain Focus**: Filters for materials with "No Copyright - United States" designation
- **Pagination Support**: Handles large result sets with automatic pagination
- **Rate Limiting**: Built-in delays to respect API server resources
- **JSON Output**: Saves each document's metadata as individual JSON files
- **Genre-Based Organization**: Processes five distinct correspondence genres systematically

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable dependency management.

```bash
# Clone the repository
git clone <repository-url>
cd talk-to-history-hpl-brown-metadata

# Install dependencies
uv sync

# Set up pre-commit hooks (optional but recommended)
uv run pre-commit install
```

## Quick Start

```bash
# Run the metadata collector
uv run main.py
```

**Expected Output:**

```
INFO:collector:Processing genre: autograph letter
INFO:collector:GET: https://repository.library.brown.edu/api/search/ with params: {...}
INFO:collector:Completed processing genre: autograph letter
...
```

Metadata files will be saved to the `./metadata` directory as individual JSON files named by document PID (e.g., `12345.json`).

### Important Note

The Brown Digital Repository uses Cloudflare protection. You may need to verify you're human by visiting `https://repository.library.brown.edu` in your browser before running the script.

## API Reference

This tool queries the [Brown Digital Repository API](https://github.com/Brown-University-Library/bdr_api_documentation/wiki) with the following parameters:

- **Collection**: `bdr:jyhg75bu` (H.P. Lovecraft Collection)
- **Creator**: `Lovecraft, H.P. (Howard Phillips)`
- **Rights**: `No Copyright - United States.`
- **Restrictions**: `Collection is open for research.`
- **Genres**:
  - autograph letter
  - autograph letter signed
  - autograph note signed
  - typed letter
  - typed letter signed

## Development

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run pre-commit checks
uv run pre-commit run --all-files
```

### Project Structure

```
├── collector.py              # Main collection logic
├── main.py                   # Entry point
├── tests/                    # Test suite
│   ├── test_build_search_query.py
│   ├── test_fetch_and_save_documents.py
│   ├── test_main.py
│   └── test_save_document.py
├── pyproject.toml           # Project dependencies
└── .pre-commit-config.yaml  # Code quality hooks
```

### Configuration

Key parameters in `collector.py`:

- `PAGE_SIZE`: Results per API request (default: 100)
- `MIN_PAUSE_SECONDS`: Minimum delay between requests (default: 1)
- `MAX_PAUSE_SECONDS`: Maximum delay between requests (default: 2)

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `uv run pytest`
2. Code is formatted: `uv run pre-commit run --all-files`
3. Coverage remains above 80%

## License

The metadata retrieved by this tool is in the **Public Domain** (No Copyright - United States). The tool itself is provided as-is for educational and research purposes.

## Acknowledgments

- **Brown University Library** for maintaining the Brown Digital Repository
- **H.P. Lovecraft Collection** at the John Hay Library
- **BDR API** for providing programmatic access to collection metadata
