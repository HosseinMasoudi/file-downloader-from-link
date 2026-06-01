import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Python Download Manager with Resume Support")

    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument(
        "-o", "--output",
        help="Output file name",
        default=None
    )
    parser.add_argument(
        "-d", "--directory",
        help="Output directory",
        default="downloads"
    )
    parser.add_argument(
        "-t", "--timeout",
        help="Request timeout in seconds",
        type=int,
        default=30
    )
    parser.add_argument(
        "-c", "--chunk-size",
        help="Chunk size in bytes",
        type=int,
        default=8192
    )

    return parser.parse_args()
