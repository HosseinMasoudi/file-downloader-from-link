# File Downloader From Link

A command-line file downloader and lightweight download manager written in Python.

This project downloads files from a given URL, displays a live progress bar, supports interrupted download resuming when the server allows it, and keeps both console and file logs. It is designed as a learning project, but follows a clean, professional structure with object-oriented code, custom exceptions, retry support, and a simple command-line interface.

## Features

- Download files from any valid HTTP or HTTPS URL
- Display download progress with `tqdm`
- Resume interrupted downloads using HTTP `Range` headers
- Automatically retry temporary server or network failures
- Support custom output file names
- Support custom output directories
- Use a `DownloadManager` class for the core download logic
- Handle errors with custom exception classes
- Log activity to both the console and a log file
- Provide a beginner-friendly `argparse` command-line interface

## Project Structure

```text
file-downloader-from-link/
|-- main.py
|-- README.md
|-- downloader/
|   |-- cli.py
|   |-- exceptions.py
|   `-- manager.py
|-- downloads/
|   `-- downloaded files
`-- logs/
    `-- downloader.log
```

### Main Files

- `main.py` configures logging, parses command-line arguments, and starts the download.
- `downloader/cli.py` defines the command-line interface using `argparse`.
- `downloader/manager.py` contains the `DownloadManager` class and download logic.
- `downloader/exceptions.py` defines custom exceptions for clearer error handling.
- `logs/downloader.log` stores file logs created while the program runs.
- `downloads/` is the default directory where downloaded files are saved.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/file-downloader-from-link.git
cd file-downloader-from-link
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install requests tqdm
```

The project uses:

- `requests` for HTTP downloads
- `tqdm` for progress bars
- `urllib3 Retry` through `requests.adapters.HTTPAdapter`
- `argparse` for command-line parsing
- `logging` for console and file logs

## Usage

Run the downloader with a file URL:

```bash
python main.py "https://example.com/file.pdf"
```

Download with a custom output filename:

```bash
python main.py "https://example.com/file.pdf" -o myfile.pdf
```

Download to a custom output directory:

```bash
python main.py "https://example.com/file.pdf" -d downloads
```

Use a custom timeout:

```bash
python main.py "https://example.com/file.pdf" -t 60
```

Use a custom chunk size:

```bash
python main.py "https://example.com/file.pdf" -c 16384
```

Combine multiple options:

```bash
python main.py "https://example.com/file.pdf" -o report.pdf -d files -t 60 -c 16384
```

## Command-Line Arguments

| Argument | Description | Default |
| --- | --- | --- |
| `url` | The URL of the file to download. | Required |
| `-o`, `--output` | Custom output file name. | File name from URL |
| `-d`, `--directory` | Directory where the downloaded file will be saved. | `downloads` |
| `-t`, `--timeout` | Request timeout in seconds. | `30` |
| `-c`, `--chunk-size` | Download chunk size in bytes. | `8192` |

## Example Output

```text
2026-06-01 12:00:00,000 - INFO - Starting download: https://example.com/file.pdf
2026-06-01 12:00:00,001 - INFO - Saving to: downloads/file.pdf
file.pdf: 100%|####################| 2.5M/2.5M [00:03<00:00, 820kB/s]
2026-06-01 12:00:03,100 - INFO - Download completed successfully.

Saved to: downloads/file.pdf
```

If a partially downloaded file already exists, the downloader checks its current size and attempts to continue from that byte position:

```text
2026-06-01 12:05:00,000 - INFO - Resuming download from byte 1048576
```

Resume support depends on the remote server. If the server does not support partial downloads and returns a normal `200 OK` response instead of `206 Partial Content`, the downloader restarts the download from the beginning.

## Error Handling

The project uses custom exceptions to make failures easier to understand and handle:

- `DownloadError` is the base exception for downloader-related errors.
- `InvalidURLError` is raised when the provided URL is missing a scheme or is not valid.
- `FileAccessError` is raised when the file cannot be created, opened, or written.
- `ServerError` is raised for server, timeout, connection, or unexpected response problems.

Common failure cases include:

- Missing `http://` or `https://` in the URL
- Invalid URL format
- Connection errors
- Request timeouts
- Unexpected HTTP status codes
- File permission or disk access problems

When an error occurs, the program logs the error and prints a clear failure message:

```text
Download failed: The request timed out.
```

## Retry Behavior

The downloader uses a `requests.Session` with `HTTPAdapter` and `urllib3 Retry` to automatically retry temporary failures.

The retry strategy currently retries up to 3 times for temporary HTTP status codes:

- `429 Too Many Requests`
- `500 Internal Server Error`
- `502 Bad Gateway`
- `503 Service Unavailable`
- `504 Gateway Timeout`

Retries are applied to safe request methods such as `GET`, `HEAD`, and `OPTIONS`, with a backoff delay between attempts.

## Logging

Logging is configured in `main.py` and writes messages to both:

- The console
- `logs/downloader.log`

The `logs` directory is created automatically when the program starts.

Logged events include:

- Download start
- Output path
- Resume attempts
- Servers that do not support resume
- Successful completion
- Download failures

Example log file path:

```text
logs/downloader.log
```

## Future Improvements

Possible improvements for future versions:

- Add automated tests
- Add checksum verification
- Add parallel or segmented downloads
- Add support for multiple URLs
- Add download speed limits
- Add better filename detection from `Content-Disposition` headers
- Add configuration through a settings file
- Publish the tool as an installable Python package
