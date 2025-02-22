"""
Constants used throughout the project.
"""

# Retry and Rate Limiting Constants
MAX_RETRIES = 5  # Maximum number of retries for requests
RATE_LIMIT_SLEEP = 1  # Sleep time in seconds for rate limiting (multiplies by 2^attempt)

# URL Components for Roblox
ROBLOX_ASSET_URL_START = "http://www.roblox.com/asset/?id="
ROBLOX_ASSET_URL_END = "</url>"
IMAGE_LOCATION_JSON_START = '{"location":"'
IMAGE_LOCATION_JSON_END = '"'

# Centralized ROUTES dictionary for URL templates
ROUTES = {
    "group_info": "https://groups.roblox.com/v1/communities/{group_id}",
    "catalog": "https://www.roblox.com/catalog/{catalog_id}",  # Specific catalog item URL
    "catalog_search": "https://catalog.roblox.com/v1/search/items",  # General catalog search API
    "base_asset": (
        "https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    ),  # Asset delivery API for clothing items
    "image_location": (
        "https://assetdelivery.roblox.com/v1/assetid/{asset_id}"
    ),  # Image location API endpoint
    # Example URL: Fetch all clothing assets by category, creator type, and sales filter
    "group_catalog": (
        "https://catalog.roblox.com/v1/search/items/details?"
        "Category=1&CreatorType=Group&CreatorTargetId={group_id}&salesTypeFilter=1"
    ),
}

# Clothing Templates for Overlays
CLOTHING_TEMPLATES = {
    "Shirt": "shirt_template.png",
    "Pants": "pants_template.png",
}

# Optional: Document URL structure for easy reference
# Example route for fetching all clothing assets from a group:
# https://www.roblox.com/catalog?Category=1&CreatorName=YOUR_GROUP_NAME&CreatorType=Group&salesTypeFilter=1
