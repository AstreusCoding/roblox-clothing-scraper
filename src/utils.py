"""
Utility module for various helper functions.
"""

import re
from typing import Optional, Tuple


def validate_clothing_id(clothing_id: str) -> str:
    """
    Validates and extracts the clothing ID from the input string.

    Args:
        clothing_id (str): The user input containing either an ID or a URL.

    Returns:
        str: The extracted clothing ID if valid, otherwise an empty string.
    """
    clothing_id = re.sub(r"[^0-9]", "", clothing_id)
    return clothing_id or ""


def extract_id_and_type_from_url(input_str: str) -> Optional[Tuple[str, str]]:
    """
    Checks if the input string is a URL and determines whether it matches the expected
    'groups' or 'catalog' pattern for Roblox URLs.

    Supported URL types:
    - https://www.roblox.com/groups/35038964/*
    - https://www.roblox.com/catalog/74366487549364/*

    Args:
        input_str (str): The user input containing a URL or asset ID.

    Returns:
        Optional[Tuple[str, str]]: A tuple containing the ID and type ('group' or 'catalog')
        if the input is a valid URL, otherwise None.
    """
    # Regular expressions to match the two URL patterns
    group_pattern = r"https://www\.roblox\.com/communities/(\d+)"
    if group_match := re.match(group_pattern, input_str):
        return group_match[1], "group"

    catalog_pattern = r"https://www\.roblox\.com/catalog/(\d+)"

    return (
        (catalog_match[1], "catalog")
        if (catalog_match := re.match(catalog_pattern, input_str))
        else None
    )
