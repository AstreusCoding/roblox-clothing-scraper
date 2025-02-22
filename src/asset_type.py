"""
This module contains the asset type class and its implementations.
"""

import re
from abc import ABC
from pathlib import Path
from typing import Dict, List, Optional, Type

from PIL import Image

import constants
from custom_logger import setup_logger
from file_handler import FileHandler

# Set up the logger for this module
logger = setup_logger(__name__)


class AssetType(ABC):
    """
    Abstract base class for different types of assets.
    """

    overlay_type: Optional[str] = None

    def __init__(self, asset_url: str, asset_image: Image.Image) -> None:
        self.asset_id = re.sub(r"[^0-9]", "", asset_url)
        if not self.asset_id:
            logger.error("Invalid asset URL provided: %s", asset_url)
            return
        self.asset_url = asset_url

        self.file_handler = FileHandler()
        self.base_url = constants.ROUTES["base_asset"].format(asset_id=self.asset_id)


        self.overlay_image_template: Optional[Image.Image] = self.get_overlay_template()
        self.asset_image: Image.Image = asset_image

    async def save_asset_image(self) -> None:
        """
        Saves the asset image to a file.
        """
        if not self.asset_image:
            logger.error("No asset image to save for asset ID: %s", self.asset_id)
            return

        self.file_handler.save_image(self.asset_image, f"{self.asset_id}.png")
        logger.info("Successfully saved asset image for asset ID: %s", self.asset_id)

    def get_overlay_template(self) -> Optional[Image.Image]:
        """
        Gets the overlay template PNG from the assets folder, based on the overlay type.

        Returns:
            Optional[Image.Image]: The overlay image if found, otherwise None.
        """
        if not self.overlay_type:
            logger.warning("Overlay type not defined for asset ID: %s", self.asset_id)
            return None

        template_filename = constants.CLOTHING_TEMPLATES.get(self.overlay_type.capitalize())
        if not template_filename:
            logger.error("No overlay template found for type: %s", self.overlay_type)
            return None

        overlay_path = Path("src", "assets", template_filename)

        if overlay_path.exists():
            logger.debug("Loading overlay template from: %s", overlay_path)
            return Image.open(overlay_path)

        logger.error("Overlay template file not found at: %s", overlay_path)
        return None

    async def overlay_image(self) -> Optional[Image.Image]:
        """
        Overlays the image with the overlay template.

        Returns:
            Image.Image: The resulting image after applying the overlay, or None if unsuccessful.
        """
        if not self.asset_image:
            logger.error("No asset image available to overlay for asset ID: %s", self.asset_id)
            return None

        if not self.overlay_image_template:
            logger.error("No overlay template available for asset ID: %s", self.asset_id)
            return None

        return Image.alpha_composite(
            self.asset_image.convert("RGBA"),
            self.overlay_image_template.convert("RGBA"),
        )


class ShirtAsset(AssetType):
    """
    Class for shirt assets.
    """

    overlay_type = "shirt"

    def print_details(self) -> None:
        """
        Print the details of the shirt asset.
        """
        logger.info("ShirtAsset with ID: %s, URL: %s", self.asset_id, self.asset_url)


class PantsAsset(AssetType):
    """
    Class for pants assets.
    """

    overlay_type = "pants"

    def print_details(self) -> None:
        """
        Print the details of the pants asset.
        """
        logger.info("PantsAsset with ID: %s, URL: %s", self.asset_id, self.asset_url)


class AssetTypeFactory:
    """
    Factory class to create instances of different asset types.
    """

    _asset_type_registry: Dict[str, Type[AssetType]] = {
        "shirt": ShirtAsset,
        "pants": PantsAsset,
    }

    @classmethod
    def create_asset(
        cls,
        asset_type: str,
        asset_url: str,
        asset_img: Image.Image,
    ) -> Optional[AssetType]:
        """
        Create an asset instance based on the asset type.

        Args:
            asset_type (str): The type of the asset (e.g., "shirt", "pants").
            asset_url (str): The URL of the asset.
            asset_img (Image.Image): The image of the asset.

        Returns:
            Optional[AssetType]: An instance of the specified asset type, or None if the
                                type is invalid.
        """
        asset_type_lower = asset_type.lower()
        if asset_class := cls._asset_type_registry.get(asset_type_lower):
            logger.debug("Creating %s for URL: %s", asset_class.__name__, asset_url)
            return asset_class(asset_url, asset_img)

        logger.error("Invalid asset type provided: %s", asset_type)
        return None

    @classmethod
    def get_supported_asset_types(cls) -> List[str]:
        """
        Get a list of supported asset types.

        Returns:
            List[str]: A list of supported asset types.
        """
        return list(cls._asset_type_registry.keys())
