"""
Description: This script downloads Roblox clothing assets
using the Roblox Asset Delivery API. It can download the
raw asset or overlay it on a shirt or pants template.
"""

import asyncio
import os
import re
from typing import Optional

import aiohttp
from PIL import Image

import constants
from file_handler import FileHandler


class RobloxAssetDownloader:
    """
    A class to download Roblox clothing assets using the Roblox Asset Delivery API.
    """

    def __init__(self) -> None:
        self.file_handler = FileHandler()

    @staticmethod
    def get_between(source: str, start: str, end: str) -> str:
        """Extract a substring between two delimiters."""
        try:
            return re.search(f"{start}(.*?){end}", source).group(1)
        except AttributeError:
            return ""

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch the content of a URL."""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to fetch: {url}")
                    return None
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"HTTP error occurred: {e}")
            return None

    async def fetch_image(
        self, session: aiohttp.ClientSession, url: str
    ) -> Optional[Image.Image]:
        """Fetch an image from a URL."""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to download image from: {url}")
                    return None
                return Image.open(await response.content.read())
        except aiohttp.ClientError as e:
            print(f"HTTP error occurred: {e}")
            return None

    async def download_image(
        self, clothing_id: str, overlay_type: Optional[str] = None
    ) -> None:
        """Download and optionally overlay a Roblox clothing asset."""
        base_url = constants.BASE_URL_TEMPLATE.format(clothing_id=clothing_id)

        async with aiohttp.ClientSession() as session:
            # Step 1: Fetch HTML response from Roblox Asset Delivery API
            html = await self.fetch(session, base_url)
            if not html:
                return

            # Step 2: Extract the Asset ID
            asset_id = self.get_between(
                html, constants.ROBLOX_ASSET_URL_START, constants.ROBLOX_ASSET_URL_END
            )
            if not asset_id:
                print("Failed to extract asset ID.")
                return

            # Step 3: Fetch image location URL
            imagelocation_url = constants.IMAGE_LOCATION_URL_TEMPLATE.format(
                asset_id=asset_id
            )
            imagelocation_response = await self.fetch(session, imagelocation_url)
            if not imagelocation_response:
                return

            imageloc = self.get_between(
                imagelocation_response,
                constants.IMAGE_LOCATION_JSON_START,
                constants.IMAGE_LOCATION_JSON_END,
            )

            # Step 4: Download the actual image
            img = await self.fetch_image(session, imageloc)
            if not img:
                return

            # Step 5: Overlay the shirt or pants template if applicable
            if overlay_type:
                template = None
                if overlay_type == "Shirt":
                    template = Image.open("shirt_template.png")
                elif overlay_type == "Pants":
                    template = Image.open("pants_template.png")

                if template:
                    img = Image.alpha_composite(
                        img.convert("RGBA"), template.convert("RGBA")
                    )

            # Step 6: Save the image
            self.file_handler.save_image(img, f"{clothing_id}.png")


async def main() -> None:
    """Main function to simulate the UI function with inputs."""
    clothing_id = input("Enter Clothing ID or Catalog URL: ")
    clothing_id = re.sub(r"[^0-9]", "", clothing_id)  # Remove non-numeric characters

    if clothing_id:
        overlay_choice = input(
            "Do you want an overlay? Enter 'Shirt' or 'Pants', or leave blank: "
        )
        overlay_choice: Optional[str] = (
            overlay_choice.strip() if overlay_choice in ["Shirt", "Pants"] else None
        )

        downloader = RobloxAssetDownloader()
        await downloader.download_image(clothing_id, overlay_choice)
    else:
        print("Invalid input. Please enter a valid Clothing ID.")


if __name__ == "__main__":
    asyncio.run(main())
