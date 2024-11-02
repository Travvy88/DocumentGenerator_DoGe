from src.url_generator import UrlGenerator

urls = UrlGenerator().generate('https://en.wikipedia.org/wiki/Main_Page', 1000, ['ru'])
for url in urls:
    print(url)
