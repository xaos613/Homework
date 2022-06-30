import argparse
import logging
import os


def get_args(args=None):
    default_path = os.path.dirname(__file__)
    parser = argparse.ArgumentParser(description='RSS parser')
    parser.add_argument('source', default=None, help='RSS URL', nargs='?')
    parser.add_argument("--version", help="Print version info and exit", action="version",
                        version="You are using %(prog)s version 1.4")
    parser.add_argument('--json', action='store_true', default=False, help='Save result as in JSON file')
    parser.add_argument('--limit', type=int, default=None, help='Limit news if this parameter provided')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="Output verbose messages")
    parser.add_argument("--colorize", help="Enables colored output mode", action="store_true", default=False)
    parser.add_argument('--date', type=str, help='Gets a date in YYYYMMDD format. Print news from the specified date.')

    parser.add_argument('--to-html', nargs='?', const=f"{default_path}", action="store",
                        help='Convert news to HTML file (provide path to folder where save export file)')
    parser.add_argument('--to-pdf', nargs='?', const=f"{default_path}", action="store",
                        help='Convert news to PDF file (provide path to folder where save export file)')

    parser.add_argument('--path', type=str, help='Gets path to save export files.', nargs='?')

    return parser.parse_args(args)


def check_args(args=None):
    args = get_args(args)
    return {
        'limit': int(args.limit) if args.limit else None,
        'json': True if args.json else False,
        'verbose': logging.INFO if args.verbose else logger_info.disable(),
        'date': args.date if args.date else None,
        'pdf': args.to_pdf if args.to_pdf else False,
        'html': args.to_html if args.to_html else False,
        'source': args.source if args.source else None,
        'color':True if args.colorize else False
    }


logger_info = logging
log_format = "%(levelname)s %(asctime)s - %(message)s"
logger_info.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt='%d:%m:%Y %H:%M:%S',
                        )
