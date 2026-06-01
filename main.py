import logging
import sys
import os

from downloader.cli import parse_args
from downloader.manager import DownloadManager
from downloader.exceptions import DownloadError


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/downloader.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    setup_logging()
    args = parse_args()

    try:
        manager = DownloadManager(
            url=args.url,
            output_dir=args.directory,
            output_name=args.output,
            chunk_size=args.chunk_size,
            timeout=args.timeout
        )
        saved_path = manager.download()
        print(f"\nSaved to: {saved_path}")

    except DownloadError as e:
        logging.error(e)
        print(f"\nDownload failed: {e}")


if __name__ == "__main__":
    main()