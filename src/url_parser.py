from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


class UrlParser:
    def parse(self, start_url, max_urls, languages):
        ptr = 0
        urls = []
        urls.append(start_url)

        pbar = tqdm(initial=1, total=max_urls)
        while len(urls) < max_urls:
            url = urls[ptr]
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve {url}: {e}")
                return

            # Parse the page content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links on the page
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                full_url = urljoin(url, href)
                if self.is_valid_url(full_url, languages) and full_url not in urls and len(urls) < max_urls:
                    urls.append(full_url)
                    pbar.update(1)
            ptr += 1
        return urls[1:]
    
    def is_valid_url(self, url, languages):
        # Check if the URL is a valid Wikipedia article URL
        parsed = urlparse(url)
        if parsed.scheme in ('http', 'https') and 'wikipedia.org' in parsed.netloc and \
            any(parsed.netloc.find(lang_element) != -1 for lang_element in languages):
            path = parsed.path
            if path.startswith('/wiki/') and not any(sub in path for sub in [':', '/wiki/Main_Page']):
                return True
        return False