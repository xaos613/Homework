import argparse
import logging
import sys

version = '0.1.0'


def print_version_and_exit():
    print(f'You are using version - {version}')
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description='RSS parser')
    parser.add_argument('source', default=None, help='RSS URL', nargs='?')
    parser.add_argument('--version', action='store_true', default=False, help='Print version info')
    parser.add_argument('--json', action='store_true', default=False, help='Save result as in JSON file')
    parser.add_argument('--limit', type=int, default=None, help='Limit news if this parameter provided')
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Output verbose messages')
    # parser.add_argument('--date', type=str, help='Gets a date in YYYYMMDD format. Print news from the specified date.')
    #
    # parser.add_argument('--clean', action='store_true', help='Clean all data from cache file')
    # parser.add_argument('--to-html', action='store_true', default=False,
    #                     help='Convert news to HTML file (provide path to folder or file *.html)')
    # parser.add_argument('--to-pdf', action='store_true', default=False,
    #                     help='Convert news to PDF file (provide path to folder or file *.pdf)')
    return parser.parse_args()


def check_args():
    args = parse_args()
    if args.version == True:
        print_version_and_exit()

    return {
        'limit': int(args.limit) if args.limit else None,
        'json': True if args.json else False,
        # 'date': args.date if args.date else None,
        'verbose': True if args.verbose else False,
        # 'pdf': True if args.to_pdf else False,
        # 'html': True if args.to_html else False,
        'source': args.source if args.source else None,
    }


logger_info = logging
log_format = "%(levelname)s %(asctime)s - %(message)s"
logger_info.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt='%d:%m:%Y %H:%M:%S',
                        )
