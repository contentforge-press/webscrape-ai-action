# WebScrape AI - GitHub Action

**Give your AI agent clean data from any URL. One URL in, structured JSON out.**

## Usage

```yaml
name: Scrape Website
on: [push]

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scrape URL
        uses: contentforge-press/webscrape-ai-action@v1
        with:
          url: 'https://example.com'
          output_format: 'json'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `url` | The URL to scrape | ✅ | - |
| `output_format` | Output format: `json` or `text` | ❌ | `json` |

## Outputs

| Output | Description |
|--------|-------------|
| `title` | Page title |
| `text` | Main text content |
| `links` | All links on the page |
| `images` | All images on the page |

## Example Output

```json
{
  "url": "https://example.com",
  "status": 200,
  "title": "Example Domain",
  "text": "Example Domain\nThis domain is for use...",
  "links": [{"text": "More info", "url": "https://iana.org"}],
  "images": []
}
```

## Use Cases

- **AI Agents** - Give your LLM real-time web data
- **RAG Systems** - Build knowledge bases from any website
- **Competitive Monitoring** - Track competitors' websites
- **Content Research** - Extract articles and blog posts

## License

MIT
