# MCP Test Project

A specialized web crawler framework designed for forum content extraction. This project focuses on efficiently crawling multiple forum boards across different websites, preserving content structure and associated media in markdown format.

## Key Features

- **Multi-Site Support**: Simultaneously crawl multiple websites with different parsing logic
- **Multi-Board Crawling**: Configure and crawl multiple boards within each website
- **Content Preservation**:
  - Converts HTML content to clean markdown format
  - Maintains original post structure and formatting
  - Downloads and organizes associated media (images, videos, audio)
  - Handles multi-page posts and replies
- **Smart Resource Management**:
  - Supports resume-able downloads for media files
  - Avoids re-downloading existing resources
  - Always refreshes post content for latest updates
- **Anti-Crawling Protection**:
  - Configurable user agent (defaults to search engine bot)
  - Random delay between requests
  - Per-board concurrent request limits
- **Progress Tracking**:
  - Overall board crawling progress
  - Individual post crawling status
  - Media download progress

## Requirements

- Python 3.7+
- Dependencies:
  ```
  aiohttp      # Async HTTP client
  aiofiles     # Async file operations
  beautifulsoup4  # HTML parsing
  markdownify  # HTML to Markdown conversion
  PyYAML      # Configuration file parsing
  tqdm        # Progress bars
  loguru      # Logging
  ```

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
  - name: "网站A"          # Website identifier
    parser: "example_site" # Parser plugin name
    boards:
      - name: "板块1"      # Board name
        url: "https://example.com/board1"
        save_dir: "boards/board1"  # Where to save content
        start_page: 1     # First page to crawl
        end_page: 3      # Last page to crawl
concurrency: 5           # Max concurrent requests per board
user_agent: "Googlebot/2.1 (+http://www.google.com/bot.html)"
delay_range: [1, 3]      # Random delay between requests (seconds)
```

### Output Structure

For each board, content is organized as follows:
```
boards/
  board1/           # Board save directory
    markdown/       # Markdown files of posts
      post-title-1.md
      post-title-2.md
    data/          # Downloaded media files
      post-title-1/
        image1.jpg
        video1.mp4
      post-title-2/
        image1.jpg
```

### Markdown Format

Posts are saved as markdown files with:
- Post title as heading
- Original post content with preserved formatting
- All replies in chronological order
- Media files referenced relatively to data directory
- Multi-page replies combined into single file

## Project Structure

- `main.py`: Core crawler implementation
- `parser_plugins/`: Website-specific parsing logic
  - `example_site.py`: Example parser implementation
- `utils/`: Helper utilities
  - `fetcher.py`: Async HTTP client with rate limiting
  - `markdown_saver.py`: Content to markdown conversion
  - `parser.py`: Base parser interface
  - `sanitize.py`: Filename sanitization
- `config.yaml`: Crawler configuration
- `requirements.txt`: Project dependencies

## Adding New Website Support

1. Create a new parser in `parser_plugins/` implementing:
   - `get_post_list_urls()`: Extract post URLs from board page
   - `parse_post_detail()`: Extract content from post page
2. Add website configuration to `config.yaml`

## Usage

Run the crawler:
```bash
python main.py
```

The crawler will:
1. Load configuration from `config.yaml`
2. Process each website and board in parallel
3. Download posts and media files
4. Save content as markdown with downloaded media

## License

MIT License