# MCP Test Project

A flexible, asynchronous web crawler framework designed for multi-site and multi-board forum content crawling. This project focuses on efficient data collection and organized content storage in markdown format.

## Features

- **Asynchronous Crawling**: Utilizes `aiohttp` for efficient concurrent requests
- **Plugin Architecture**: Extensible parser plugins for different website structures
- **Markdown Export**: Converts HTML content to clean markdown format
- **Resource Management**: Automatically downloads and manages associated resources (images, videos, etc.)
- **Pagination Support**: Handles multi-page posts and replies
- **Configurable**: YAML-based configuration for easy customization
- **Rate Limiting**: Built-in delay and concurrency control to respect website policies

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project uses `config.yaml` for configuration:

```yaml
websites:
  - name: "Website Name"
    parser: "parser_plugin_name"
    boards:
      - name: "Board Name"
        url: "https://example.com/board"
        save_dir: "boards/board1"
        start_page: 1
        end_page: 3
concurrency: 5
user_agent: "Your User Agent"
delay_range: [1, 3]
```

### Configuration Parameters

- `websites`: List of websites to crawl
  - `name`: Website identifier
  - `parser`: Parser plugin to use
  - `boards`: List of boards to crawl
    - `url`: Board URL
    - `save_dir`: Directory to save crawled content
    - `start_page`/`end_page`: Page range to crawl
- `concurrency`: Maximum concurrent requests
- `user_agent`: User agent string for requests
- `delay_range`: Random delay range between requests [min, max] in seconds

## Usage

Run the crawler:

