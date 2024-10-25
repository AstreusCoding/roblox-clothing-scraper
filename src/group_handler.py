"""
This module contains the GroupHandler class, which is
responsible for processing Roblox groups and fetching
all clothing asset IDs from a specified group.
Classes:
    GroupHandler: A class to process Roblox groups
                and fetch all clothing asset IDs from the group.
Functions:
    __init__(self) -> None:
        Initializes the GroupHandler instance and sets up the API handler.
    fetch_all_clothing_ids(self, group_id: str) -> Optional[List[str]]:

"""

from typing import List, Optional

import constants
from api_handler import APIHandler
from custom_logger import setup_logger

# Set up the logger for this module
logger = setup_logger(__name__)


class GroupHandler:
    """
    A class to process Roblox groups and fetch all clothing asset IDs from the group.
    """

    def __init__(self) -> None:
        self.api_handler = APIHandler()

    async def fetch_all_clothing_ids(self, group_id: str) -> Optional[List[str]]:
        """
        Fetches all clothing asset IDs from the given Roblox group.

        Args:
            group_id (str): The ID of the Roblox group.

        Returns:
            Optional[List[str]]: A list of clothing asset IDs if successful, otherwise None.
        """
        url = constants.ROUTES["group_catalog"].format(group_id=group_id)
        all_assets = await self.api_handler.fetch_paginated_data(
            url, params={"sortOrder": "Ascend"}
        )

        if not all_assets:
            logger.error("Failed to fetch clothing assets for group ID: %s", group_id)
            return None

        clothing_ids = [str(asset["id"]) for asset in all_assets if "id" in asset]
        logger.info("Fetched %d clothing asset IDs for group ID: %s", len(clothing_ids), group_id)
        return clothing_ids


# Example usage:
# group_handler = GroupHandler()
# clothing_ids = await group_handler.fetch_all_clothing_ids("YOUR_GROUP_ID")