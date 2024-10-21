"""
Description: This handler class is responsible for handling file operations.
It provides a method to create the download directory. And methods to save
files and images to the download directory.
"""

import os

from PIL import Image


class FileHandler:
    """A class to handle file operations."""

    def __init__(self) -> None:
        self.download_dir = self.create_download_directory()

    @staticmethod
    def create_download_directory() -> str:
        """Create and return the download directory path."""
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)
        return download_dir

    def save_image(self, img: Image.Image, filename: str) -> None:
        """Save an image to the download directory."""
        img.save(os.path.join(self.download_dir, filename), "PNG")
        print(f"Image saved to {os.path.join(self.download_dir, filename)}")
