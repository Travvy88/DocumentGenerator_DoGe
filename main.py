import argparse
import cProfile
import json
from pathlib import Path
from src.manager import Manager


def create_parser():
    parser = argparse.ArgumentParser(description="Manager Configuration")
    
    parser.add_argument('--out_dir', type=str, required=True,
                        help='Output directory for saving results')
    parser.add_argument('--remove_excisting_dir', type=bool, default=False,
                        help='If out_dir excists, delete the folder and files before creating a new one')
    parser.add_argument('--max_pages', type=int, default=100,
                        help='Maximum number of pages to process (default: 100)')
    parser.add_argument('--image_size', type=int, default=244,
                        help='Size of images to process (default: 244)')
    parser.add_argument('--start_page', type=str, default='https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0',
                        help='Starting page URL (default: Wikipedia main page in Russian)')
    parser.add_argument('--languages', type=str, nargs='+', default=['ru'],
                        help='Languages to consider (default: ru)')
    parser.add_argument('--max_urls', type=int, default=100,
                        help='Maximum number of URLs to process (default: 100)')
    parser.add_argument('--num_processes', type=int, default=1,
                        help='Number of processes to use (default: 1)')
    parser.add_argument('--ports', type=str, default='2000,2001',
                        help='Comma-separated list of ports to use (default: 2000,2001). Number of ports \
                            should be 2 times larger than num_processes')

    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    with open('docx_config.json', 'r') as f:
        docx_config = json.load(f)

    manager = Manager(
        docx_config=docx_config,
        out_dir=Path(args.out_dir),
        remove_excisting_dir=args.remove_excisting_dir,
        max_pages=args.max_pages,
        image_size=args.image_size,
        start_page=args.start_page,
        languages=tuple(args.languages),
        max_urls=args.max_urls,
        num_processes=args.num_processes,
        ports=args.ports.split(',')
    )
    manager.generate()
