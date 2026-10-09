#!/usr/bin/env python3
"""
WebScrape AI GitHub Action
Give your AI agent clean data from any URL.
"""

import sys
import json
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape(url: str) -> dict:
    """Scrape a URL and return structured data."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    }
    
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Title
        title = soup.title.get_text(strip=True) if soup.title else ''
        
        # Main text
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        # Links
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(url, a['href'])
            if full_url.startswith(('http://', 'https://')):
                links.append({
                    'text': a.get_text(strip=True),
                    'url': full_url,
                })
        
        # Images
        images = []
        for img in soup.find_all('img', src=True):
            full_url = urljoin(url, img['src'])
            if full_url.startswith(('http://', 'https://')):
                images.append({
                    'alt': img.get('alt', ''),
                    'url': full_url,
                })
        
        return {
            'url': url,
            'status': response.status_code,
            'title': title,
            'text': '\n'.join(lines[:50]),
            'links': links[:30],
            'images': images[:10],
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <url> [output_format]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    
    try:
        result = scrape(url)
        
        if output_format == 'text':
            print(f"Title: {result['title']}")
            print(f"\nContent:\n{result['text']}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Set GitHub outputs
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            f.write(f"title={result['title']}\n")
            f.write(f"text={result['text'][:500]}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import os
    main()
