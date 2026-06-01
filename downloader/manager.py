import os
import logging
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

from .exceptions import InvalidURLError, FileAccessError, ServerError


class DownloadManager:
    def __init__(self, url, output_dir="downloads", output_name=None, chunk_size=8192, timeout=30):
        self.url = url
        self.output_dir = output_dir
        self.output_name = output_name
        self.chunk_size = chunk_size
        self.timeout = timeout

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        self.session = self._create_session()

        os.makedirs(self.output_dir, exist_ok=True)

    def _create_session(self):
        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _get_filename_from_url(self):
        parsed = urlparse(self.url)
        filename = os.path.basename(parsed.path)
        if not filename:
            return "downloaded_file"
        return filename

    def _get_output_path(self):
        filename = self.output_name if self.output_name else self._get_filename_from_url()
        return os.path.join(self.output_dir, filename)

    def download(self):
        output_path = self._get_output_path()

        existing_file_size = 0
        mode = "wb"
        request_headers = self.headers.copy()

        if os.path.exists(output_path):
            existing_file_size = os.path.getsize(output_path)
            if existing_file_size > 0:
                request_headers["Range"] = f"bytes={existing_file_size}-"
                mode = "ab"
                logging.info(f"Resuming download from byte {existing_file_size}")

        try:
            with self.session.get(
                self.url,
                stream=True,
                headers=request_headers,
                timeout=self.timeout
            ) as response:

                if response.status_code not in (200, 206):
                    raise ServerError(f"Unexpected status code: {response.status_code}")

                if existing_file_size > 0 and response.status_code == 200:
                    logging.warning("Server does not support resume. Restarting download from beginning.")
                    existing_file_size = 0
                    mode = "wb"

                total_size = int(response.headers.get("content-length", 0))
                if response.status_code == 206:
                    total_size += existing_file_size

                logging.info(f"Starting download: {self.url}")
                logging.info(f"Saving to: {output_path}")

                with open(output_path, mode) as file, tqdm(
                    total=total_size,
                    initial=existing_file_size,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=os.path.basename(output_path)
                ) as progress_bar:

                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))

            logging.info("Download completed successfully.")
            return output_path

        except requests.exceptions.MissingSchema:
            raise InvalidURLError("Invalid URL format. Did you forget http:// or https:// ?")

        except requests.exceptions.InvalidURL:
            raise InvalidURLError("The URL provided is invalid.")

        except requests.exceptions.Timeout:
            raise ServerError("The request timed out.")

        except requests.exceptions.ConnectionError:
            raise ServerError("Connection error occurred while downloading.")

        except OSError as e:
            raise FileAccessError(f"File error: {e}")

        except requests.exceptions.RequestException as e:
            raise ServerError(f"Request failed: {e}")
