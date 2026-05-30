import requests
from tqdm import tqdm
from urllib.parse import urlparse
import os

URL = input("Enter the URL of the file to download: \n")

filename = os.path.basename(urlparse(URL).path)
if not filename:
    filename = "downloaded_file"
    
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(URL, stream=True, headers=headers, timeout=30)
    response.raise_for_status()

    total_length = int(response.headers.get("content-length", 0))

    with open(filename, "wb") as f, tqdm(
        total=total_length,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=filename
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))

    print("Download completed!")
    print(f"Saved as: {filename}")

except requests.exceptions.RequestException as e:
    print(f"Download failed: {e}")