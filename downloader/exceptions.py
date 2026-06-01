class DownloadError(Exception):
    """Base exception for download errors."""
    pass

class InvalidURLError(DownloadError):
    """Raised when the provided URL is invalid."""
    pass

class FileAccessError(DownloadError):
    """Raised when file cannot be created or written."""
    pass

class ServerError(DownloadError):
    """Raised when the server response is invalid."""
    pass