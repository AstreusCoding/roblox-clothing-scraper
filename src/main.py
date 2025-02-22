"""
Main module to run the CLI interface and handle asset downloading.

main.py
"""

import asyncio

from console_interface import CLIInterface
from custom_logger import setup_logger
from group_handler import GroupHandler
from roblox_asset_downloader import RobloxAssetDownloader
from utils import extract_id_and_type_from_url, validate_clothing_id

# Set up the logger for this module
logger = setup_logger(__name__)

information_list = [
    "Enter a Clothing ID or URL to download the asset.",
    "If you enter a group ID or URL, it will download their clothing. ",
    "The assets will be saved as a PNG file in the 'downloads' folder.",
]


async def handle_group(interface, group_id: str) -> None:
    """
    Asynchronously handles the downloading of a Roblox group's clothing given its ID.
    Args:
        interface: An object that provides methods to display output to the user.
        group_id (str): The ID of the Roblox group to download clothing from.
    Returns:
        None
    Raises:
        asyncio.TimeoutError: If the download process times out.
        ValueError: If the group ID is invalid or another error occurs during processing.
    Logs:
        Logs successful downloads and errors encountered during the download process.
    """

    if group_id:
        group_handler = GroupHandler()
        try:
            clothing_ids = await group_handler.fetch_all_clothing_ids(group_id)
            if clothing_ids:
                for clothing_id in clothing_ids:
                    await handle_asset(interface, clothing_id)
            else:
                interface.display_output("No clothing assets found in the group.")
                logger.warning("No clothing assets found in the group.")
        except (asyncio.TimeoutError, ValueError) as e:
            interface.display_output(f"An error occurred: {str(e)}")
            logger.error("An error occurred while downloading the group's clothing: %s", str(e))
    else:
        interface.display_output("Invalid input. Please enter a valid Group ID or URL.")
        logger.warning("User input was invalid, no valid group ID found.")


async def handle_asset(interface, asset_id: str) -> None:
    """
    Asynchronously handles the downloading of a Roblox asset given its ID.
    Args:
        interface: An object that provides methods to display output to the user.
        asset_id (str): The ID of the Roblox asset to be downloaded.
    Returns:
        None
    Raises:
        asyncio.TimeoutError: If the download process times out.
        ValueError: If the asset ID is invalid or another error occurs during processing.
    Logs:
        Logs successful downloads and errors encountered during the download process.
    """

    if asset_id:
        downloader = RobloxAssetDownloader()
        try:
            await downloader.process_asset(asset_id)
            interface.display_output(f"Successfully downloaded asset: {asset_id}")
            logger.info("Successfully downloaded asset: %s", asset_id)
        except (asyncio.TimeoutError, ValueError) as e:
            interface.display_output(f"An error occurred: {str(e)}")
            logger.error("An error occurred while downloading the asset: %s", str(e))
    else:
        interface.display_output("Invalid input. Please enter a valid Clothing ID or URL.")
        logger.warning("User input was invalid, no valid asset ID found.")


async def handle_download() -> None:
    """
    Handles the main workflow:
    - Getting user input,
    - Validating the input,
    - Downloading the Roblox asset.

    Returns:
        None
    """
    interface = CLIInterface()
    interface.clear_screen()
    interface.display_program_name()
    interface.display_output("Welcome to the Clothing Scraper!")
    interface.display_information_list(information_list)

    clothing_id_input = interface.get_input("Enter a Clothing ID or URL: ")

    asset_id, asset_type = None, None
    if result := extract_id_and_type_from_url(clothing_id_input):
        asset_id, asset_type = result
        interface.display_output(f"URL identified as {asset_type} with ID {asset_id}")
        logger.info("Valid URL input. Identified as %s with ID %s", asset_type, asset_id)
    else:
        # Fallback to regular ID validation if not a valid URL
        asset_id = validate_clothing_id(clothing_id_input)
        if asset_id:
            logger.info("Valid clothing ID input: %s", asset_id)
        else:
            logger.error("Invalid input. Failed to extract a valid ID.")
            interface.display_output("Invalid input. Please enter a valid Clothing ID or URL.")
            return

    if asset_type is None or asset_id is None:
        error_msg = f"asset type: {asset_type} : asset id: {asset_id}"
        logger.error(error_msg)
        return
    
    if asset_type != "group":
        await handle_asset(interface, asset_id)
    else:
        await handle_group(interface, asset_id)


async def main() -> None:
    """Main function to start the application."""
    while True:
        await handle_download()
        break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except (asyncio.TimeoutError, ValueError) as e:
        logger.error("An error occurred: %s", e)
    except (OSError, RuntimeError) as e:
        logger.error("Unexpected error occurred: %s", e)
