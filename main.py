import argparse
import cProfile
import json
from pathlib import Path
from src.manager import Manager


def create_parser():
    parser = argparse.ArgumentParser(description="Manager Configuration")
    
    parser.add_argument('--out_dir', type=str, required=True,
                        help='Output directory for saving results')
    parser.add_argument('--remove_existing_dir', action='store_true',
                        help='If out_dir exists, delete the folder and files before creating a new one')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    parser.add_argument('--image_size', type=int, default=244,
                        help='Size of the final images (default: 244)')
    parser.add_argument('--start_page', type=str, default='https://en.wikipedia.org/wiki/Main_Page',
                        help='Starting page URL (default: Wikipedia main page)')
    parser.add_argument('--languages', type=str, nargs='+', default=['en'],
                        help='Permitted languages. Other languages will be ignored (default: English)')
    parser.add_argument('--max_urls', type=int, default=16,
                        help='Maximum number of URLs to process (default: 100)')
    parser.add_argument('--num_processes', type=int, default=1,
                        help='Number of processes to use (default: 1)')
    parser.add_argument('--max_threads', type=int, default=3,
                        help='Maximum threads inside a process (default: 3)')
    parser.add_argument('--ports', type=str, nargs='+', default=[8145, 8146],
                        help='List of ports to use (default: [8145, 8146]). Number of ports \
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
        remove_existing_dir=args.remove_existing_dir,
        debug=args.debug,
        image_size=args.image_size,
        start_page=args.start_page,
        languages=tuple(args.languages),
        max_urls=args.max_urls,
        num_processes=args.num_processes,
        max_threads=args.max_threads,
        ports=tuple(args.ports)
    )
    manager.generate()
