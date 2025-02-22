"""
A class to download Roblox clothing assets using the Roblox Asset Delivery API.

This class provides methods to fetch clothing assets from Roblox,
extract necessary information, and download images, optionally
overlaying them on shirt or pants templates.

Attributes:
    file_handler (FileHandler): An instance of FileHandler to manage file operations.
    api_handler (APIHandler): An instance of APIHandler to handle API requests.

Methods:
    fetch_asset(asset_url: str) -> Optional[dict]:
        Fetches the asset data from a given URL.
    fetch_image_location(asset_id: str) -> Optional[str]:
        Fetches the image location for the given asset ID.
    download_asset(url: str) -> Optional[Image.Image]:
        Downloads an image from the given URL.
    process_asset(clothing_id: str) -> None:
        Processes a clothing asset by fetching its image and saving it.

roblox_asset_downloader.py
"""

import io
import re
from typing import Optional

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError

import constants
from api_handler import APIHandler
from asset_type import AssetTypeFactory
from custom_logger import setup_logger
from file_handler import FileHandler
from utils import validate_clothing_id

# Set up the logger for this module
logger = setup_logger(__name__)


class RobloxAssetDownloader:
    """
    A class to download Roblox clothing assets using the Roblox Asset Delivery API.

    This class provides methods to fetch clothing assets from Roblox,
    extract necessary information, and download images, optionally
    overlaying them on shirt or pants templates.

    Attributes:
        file_handler (FileHandler): An instance of FileHandler to manage file operations.
        api_handler (APIHandler): An instance of APIHandler to handle API requests.
    """

    def __init__(self) -> None:
        self.file_handler = FileHandler()
        self.api_handler = APIHandler()

    async def fetch_asset(self, asset_url: str) -> Optional[dict]:
        """
        Fetches the asset data from the given asset URL.

        Args:
            asset_url (str): The URL of the asset to fetch.

        Returns:
            Optional[dict]: A dictionary containing the asset data if successful, otherwise None.
        """
        asset_id = re.sub(r"[^0-9]", "", asset_url)
        if not asset_id:
            logger.error("Invalid asset URL provided: %s", asset_url)
            return None

        asset_delivery_url: str = constants.ROUTES["base_asset"].format(asset_id=asset_id)

        # Fetch the asset page as text using the API handler's fetch_text method
        data = await self.api_handler.fetch_text(asset_delivery_url)
        if not data:
            logger.error("Failed to fetch asset data from: %s", asset_delivery_url)
            return None

        # Parse the HTML response using BeautifulSoup
        data_soup = BeautifulSoup(data, "html.parser")

        if not data_soup:
            logger.error("Failed to parse asset data from: %s", asset_delivery_url)
            return None

        content_name = data_soup.find("content").get("name")
        template_id = data_soup.find("url").text

        if not content_name or not template_id:
            logger.error("Failed to extract asset data from: %s", asset_delivery_url)
            return None

        # Validate and extract the template ID to ensure it's a valid clothing ID
        template_id = validate_clothing_id(template_id)

        discovered_asset = {
            "asset id": asset_id,
            "content name": content_name,
            "template id": template_id,
        }

        logger.debug("Discovered Asset: %s", discovered_asset)

        # Map content names like "PantsTemplate" and "ShirtTemplate" to easier names
        if "PantsTemplate" in discovered_asset["content name"]:
            discovered_asset["content name"] = "pants"
        elif "ShirtTemplate" in discovered_asset["content name"]:
            discovered_asset["content name"] = "shirt"

        return discovered_asset

    async def fetch_image_location(self, asset_id: str) -> Optional[str]:
        """
        Fetches the image location URL for a given asset ID.

        Args:
            asset_id (str): The ID of the asset for which to fetch the image location.

        Returns:
            Optional[str]: The image location URL if found, otherwise None.
        """
        imagelocation_url: str = constants.ROUTES["image_location"].format(asset_id=asset_id)
        logger.debug("Fetching image location from: %s", imagelocation_url)

        # Use fetch_json to get the image location JSON response
        response = await self.api_handler.fetch_json(imagelocation_url)
        if not response:
            logger.error("Failed to fetch image location for asset ID: %s", asset_id)
            return None

        return self.extract_image_location_from_json(response)

    def extract_image_location_from_json(self, json_dict: dict) -> Optional[str]:
        """
        Extracts the image location URL from the given JSON response.

        Args:
            json_dict (dict): The JSON content to search for the image location.

        Returns:
            Optional[str]: The extracted image location URL if found, otherwise None.
        """
        try:
            return json_dict["location"]
        except KeyError:
            logger.error("No location found in the JSON response.")
            return None

    async def download_asset(self, url: str) -> Optional[Image.Image]:
        """
        Asynchronously fetches an image from the given URL.
        """
        logger.debug("Downloading asset image from: %s", url)
        try:
            # Fetch the image bytes (ensure binary mode)
            image_bytes = await self.api_handler.fetch_image(url)
            if not image_bytes:
                logger.error("Failed to download image from: %s", url)
                return None
            # Ensure we're treating it as binary data
            asset_img = Image.open(io.BytesIO(image_bytes))
            asset_img.load()  # Force loading of the image
            
            return asset_img
        except (IOError, OSError, UnidentifiedImageError) as e:
            logger.error("Error processing image from %s: %s", url, str(e))
            return None


    async def process_asset(self, clothing_id: str) -> None:
        """
        Processes the given clothing asset URL to download the image.

        Args:
            clothing_id (str): The ID of the clothing asset to download.

        Returns:
            None
        """
        # Fetch the asset data (e.g., asset ID, template, etc.)
        asset_data = await self.fetch_asset(clothing_id)
        if not asset_data:
            logger.error("No asset data found for clothing ID: %s", clothing_id)
            return
        logger.info("asset data found")
        # Fetch the image location URL
        image_location = await self.fetch_image_location(asset_data["template id"])
        if not image_location:
            return

        logger.info("Downloading image from URL: %s", image_location)
        # Download the image from the URL
        asset_img = await self.download_asset(image_location)
        if not asset_img:
            return

        # Create an asset instance for handling overlay operations
        asset_type = asset_data["content name"]
        asset_instance = AssetTypeFactory.create_asset(asset_type, clothing_id, asset_img)

        if not asset_instance:
            logger.error("Failed to create asset instance for asset type: %s", asset_type)
            return

        # Overlay the image on the template (if needed)
        overlayed_image = await asset_instance.overlay_image()
        if not overlayed_image:
            logger.error("Failed to overlay image on %s template.", asset_type)
            return

        # Save the overlayed image
        await asset_instance.save_asset_image()
        logger.info("Successfully processed and saved asset for clothing ID: %s", clothing_id)

        await self.api_handler.close()
        logger.debug("API handler closed.")
