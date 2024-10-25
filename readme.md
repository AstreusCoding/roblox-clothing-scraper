# Roblox Clothing Scraper

This project is a Python-based tool for downloading clothing assets from Roblox using the Roblox API. The application provides a user-friendly console interface for interacting with the API, enabling both individual asset downloads and mass downloads for entire Roblox groups.

## TODO

- **Multithreading**: Implement multithreading or asynchronous processing to speed up downloads, especially for large groups.
- **Code Cleanup**: Refactor and optimize existing code for improved readability and maintainability.
- **GUI**: Develop a graphical user interface (GUI) to make the application more accessible to users unfamiliar with CLI.
- **Proxies**: Add support for proxies to avoid IP restrictions and handle large-scale scraping.
- **Global Scraper**: Create a feature to randomly scrape clothing assets based on customizable filters (e.g., recently published, best-selling, most favorited, relevance).
- **Improved File Management**: Enhance file organization for downloaded assets, such as categorizing by asset type, date, or other metadata.
- **Download clothing metadata**: Retrieve and store additional information about downloaded assets, such as asset name, creator, price, etc.
- **Asset Search**: Enable asset search functionality to find specific items based on keywords, tags, or other criteria.

## Features

- **Single Asset Download**: Download individual clothing items by providing their ID or URL.
- **Group Asset Download**: Download all clothing assets associated with a specific Roblox group.
- **Easy to Use**: Follow the on-screen instructions within the console interface to interact with the application.
- **File Management**: Downloaded assets are saved as PNG files in the `downloads` folder for easy access.

## Quick Start

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Run the `run.bat` script**:
    - The `run.bat` script automates setup and execution.
    - It will:
        - Create and activate a virtual environment.
        - Install necessary dependencies.
        - Launch the console interface.

    ```sh
    run.bat
    ```

3. **Follow On-Screen Instructions**:
   - Enter an asset ID or URL to download individual items.
   - Enter a group ID or URL to download all clothing items from a group.

## Project Structure

```plaintext
.
├── src/
│   ├── api_handler.py            # Manages API interactions with Roblox
│   ├── asset_type.py             # Defines asset types for processing
│   ├── console_interface.py      # Provides the CLI for user interaction
│   ├── constants.py              # Contains constants used across the project
│   ├── custom_logger.py          # Implements custom logging
│   ├── file_handler.py           # Manages file operations for saving assets
│   ├── group_handler.py          # Handles group-related operations
│   ├── main.py                   # Main entry point of the application
│   ├── roblox_asset_downloader.py # Downloads assets from Roblox
│   └── utils.py                  # Utility functions (e.g., validation)
├── downloads/                    # Folder where downloaded assets are stored
├── requirements.txt              # Lists all dependencies
├── run.bat                       # Batch script for running and setting up the project
└── README.md                     # Project documentation
```

## Installation and Setup

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   - Run `run.bat` to create a virtual environment and install dependencies, or manually use:
     ```sh
     python -m venv venv
     venv\Scripts\activate  # On Windows
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   ```sh
   run.bat
   ```

## Requirements

- Python 3.x
- **Dependencies**:
  - Install via `requirements.txt`

## Modules Overview

| Module                   | Description                                                 |
|--------------------------|-------------------------------------------------------------|
| **`api_handler.py`**     | Handles API calls to Roblox for retrieving asset data.      |
| **`asset_type.py`**      | Defines asset processing types (e.g., shirts, pants).       |
| **`console_interface.py`** | Provides a user interface for entering asset and group data. |
| **`constants.py`**       | Holds constant values (URLs, retry settings).               |
| **`custom_logger.py`**   | Manages custom logging for the application.                 |
| **`file_handler.py`**    | Saves downloaded assets as PNG files in the `downloads/` folder. |
| **`group_handler.py`**   | Fetches all clothing assets in a group and initiates download. |
| **`main.py`**            | Main entry point for the CLI application.                   |
| **`roblox_asset_downloader.py`** | Downloads individual assets from Roblox.            |
| **`utils.py`**           | Helper functions for input validation and ID extraction.    |

## License

This project is licensed under the MIT License. See the LICENSE file for details.