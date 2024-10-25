"""
This module provides an APIHandler class for handling asynchronous fetching of JSON, text,
and image data from URLs.

Classes:
    APIHandler: A class to handle asynchronous fetching of JSON, text, and image data from URLs.

Functions:
    __init__(self): Initializes the APIHandler instance.
    _is_json_response(self, response: aiohttp.ClientResponse) -> bool: Checks if the response
        content type is JSON.
    _handle_response_status(self, response: aiohttp.ClientResponse, attempt: int) -> 
        Dict[str, Any]: Handles the response status and logs any errors.
    _get(self, session: aiohttp.ClientSession, url: str, 
        params: Optional[Dict[str, str]] = None, max_retries: int = 5) -> 
        Union[dict, str, None]: Sends a GET request to the given URL and returns the JSON response.
    get_session(self) -> aiohttp.ClientSession: Gets or creates an aiohttp.ClientSession instance.
    fetch_json(self, url: str, params: Optional[Dict[str, str]] = None, retries: int = 5) -> 
        Union[dict, None]: Fetches JSON data from the given URL using aiohttp with a retry mechanism
    fetch_text(self, url: str, retries: int = 5) -> Optional[str]: Fetches text data from the
        given URL using aiohttp with a retry mechanism.
    fetch_image(self, url: str) -> Optional[bytes]: Fetches image data from the given URL.
    fetch_paginated_data(self, url: str, params: dict, limit: int = 10, retries: int = 5) -> 
        List[dict]: Fetches paginated data from the given URL, handling pagination and returning
        all results.
    close(self) -> None: Closes the aiohttp.ClientSession if it is open.
"""

import asyncio
import ssl
import time
from logging import Logger
from typing import Any, Callable, Dict, List, Optional, Union

import aiohttp
import certifi

import constants
from custom_logger import setup_logger

ssl_context = ssl.create_default_context(cafile=certifi.where())

STATUS_MAP: Dict[int, Union[Callable[[Any], str], str]] = {
    200: lambda data: f"Request to {data['url']} using {data['method']} was successful",
    429: lambda data: (
        f"Request to {data['url']} using {data['method']} was rate limited. "
        f"Retrying in {data['potential_wait_time']} seconds..."
    ),
    500: lambda data: (
        f"Request to {data['url']} using {data['method']} failed due to a server error"
    ),
    502: lambda data: (
        f"Request to {data['url']} using {data['method']} failed due to a bad gateway"
    ),
    503: lambda data: (
        f"Request to {data['url']} using {data['method']} failed due to a service unavailable error"
    ),
    504: lambda data: (
        f"Request to {data['url']} using {data['method']} failed due to a gateway timeout"
    ),
    404: lambda data: (
        f"Request to {data['url']} using {data['method']} failed due to a not found error"
    ),
}


class APIHandler:
    """
    A class to handle asynchronous fetching of JSON, text, and image data from URLs.
    It includes retry mechanisms and functionality for handling paginated data fetching.
    """

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger: Logger = setup_logger(__name__)

    async def _is_json_response(self, response: aiohttp.ClientResponse) -> bool:
        """
        Check if the response content type is JSON.
        """
        return "application/json" in response.headers.get("Content-Type", "")

    async def _handle_response_status(
        self, response: aiohttp.ClientResponse, attempt: int
    ) -> Dict[str, Any]:
        """
        Handle the response status and log any errors.
        """
        request_data = {
            "url": response.url,
            "method": response.method,
            "status": response.status,
            "current_attempt": attempt,
            "time": time.time(),
            "potential_wait_time": constants.RATE_LIMIT_SLEEP**attempt,
        }
        if response.status in STATUS_MAP:
            status_handler = STATUS_MAP[response.status]
            log_message = (
                status_handler(request_data) if callable(status_handler) else status_handler
            )
            self.logger.debug(log_message)
        else:
            # Log an error for statuses that are not in STATUS_MAP
            self.logger.error(
                "Request to %s using %s failed with status %s",
                response.url,
                response.method,
                response.status,
            )

        if response.status == 429:
            await asyncio.sleep(request_data["potential_wait_time"])

        return request_data

    async def _get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        params: Optional[Dict[str, str]] = None,
        max_retries: int = 5,
    ) -> Union[dict, str, None]:
        """
        Send a GET request to the given URL and return the JSON response.
        """
        failed_attempts: list = [dict]
        for attempt in range(max_retries):
            try:
                async with session.get(url, params=params, ssl=ssl_context) as response:
                    status_response = await self._handle_response_status(response, attempt)

                    if response.status != 200:
                        failed_attempts.append(status_response)
                        continue

                    if self._is_json_response(response):
                        return await response.json()
                    else:
                        return await response.text()

            except aiohttp.ClientError as e:
                wait_time = constants.RATE_LIMIT_SLEEP**attempt
                self.logger.error(
                    "HTTP error occurred while sending "
                    "GET request to %s: %s. Retrying in %s seconds...",
                    url,
                    e,
                    wait_time,
                )
                await asyncio.sleep(wait_time)

        self.logger.error("Exceeded retries. Failed to fetch JSON from %s.", url)
        return None

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp.ClientSession instance."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def fetch_json(
        self, url: str, params: Optional[Dict[str, str]] = None, retries: int = 5
    ) -> Union[dict, None]:
        """
        Fetch JSON data from the given URL using aiohttp with a retry mechanism.
        """
        session = await self.get_session()
        response = await self._get(session, url, params, retries)

        if response and isinstance(response, dict):
            self.logger.debug("Successfully fetched JSON from %s", url)
            return response

        self.logger.error("Failed to fetch JSON from %s", url)
        return None

    async def fetch_text(self, url: str, retries: int = 5) -> Optional[str]:
        """
        Fetch text data from the given URL using aiohttp with a retry mechanism.
        """
        session = await self.get_session()
        for attempt in range(retries):
            try:
                async with session.get(url, ssl=ssl_context) as response:
                    if response.status == 200:
                        self.logger.debug("Successfully fetched text from %s", url)
                        return await response.text()
                    elif response.status == 429:  # Handle rate limiting
                        wait_time = 2**attempt
                        self.logger.warning(
                            "Rate limited when fetching text from %s. Retrying in %s seconds...",
                            url,
                            wait_time,
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        self.logger.error(
                            "Failed to fetch text from %s. Status: %s",
                            url,
                            response.status,
                        )
                        return None
            except aiohttp.ClientError as e:
                wait_time = 2**attempt
                self.logger.error(
                    """HTTP error occurred while fetching 
                    text from %s: %s. Retrying in %s seconds...""",
                    url,
                    e,
                    wait_time,
                )
                await asyncio.sleep(wait_time)

        self.logger.error("Exceeded retries. Failed to fetch text from %s.", url)
        return None

    async def fetch_image(self, url: str) -> Optional[bytes]:
        """
        Fetches image data from the given URL.

        Args:
            url (str): The URL to fetch the image from.

        Returns:
            Optional[bytes]: The image data as bytes, or None if an error occurs.
        """
        session = await self.get_session()
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    self.logger.debug("Successfully fetched image from %s", url)
                    return await response.read()
                else:
                    self.logger.error("Failed to fetch image. Status code: %s", response.status)
                    return None
        except aiohttp.ClientError as e:
            self.logger.error("HTTP error occurred while fetching image from %s: %s", url, str(e))
            return None

    async def fetch_paginated_data(
        self, url: str, params: dict, limit: int = 10, retries: int = 5
    ) -> List[dict]:
        """
        Fetch paginated data from the given URL, handling pagination and returning all results.
        """
        all_data: List[dict] = []
        params["limit"] = str(limit)
        page_cursor = None

        while True:
            if page_cursor:
                params["cursor"] = page_cursor

            response = await self.fetch_json(url, params, retries)
            if not response or "data" not in response:
                break

            all_data.extend(response["data"])
            page_cursor = response.get("nextPageCursor")

            if not page_cursor:
                break

        self.logger.debug("Fetched a total of %s items from %s", len(all_data), url)
        return all_data

    async def close(self) -> None:
        """Closes the aiohttp.ClientSession if it is open."""
        if self.session and not self.session.closed:
            await self.session.close()
