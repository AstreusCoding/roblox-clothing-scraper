"""
Module containing the command-line interface (CLI)
implementation of the `Interface` class.
"""

import enum
import os
import platform

from interface import Interface


class CliMenuState(enum.Enum):
    """
    Enum representing the different states of the menu in the clothing scraper application.
    Attributes:
        MAIN_MENU (int): Represents the main menu state.
        DOWNLOADING_MENU (int): Represents the downloading menu state.
        SETTINGS_MENU (int): Represents the settings menu state.
    """

    MAIN_MENU = 1
    DOWNLOADING_MENU = 2
    SETTINGS_MENU = 3


class CLIInterface(Interface):
    """
    Command-line interface (CLI) implementation of the `Interface` class.
    This class handles user input and output through the terminal.

    The output is handled by the `render_to_terminal` method which refreshes
    the terminal screen with the current state of the program.
    """

    PROGRAM_NAME = "Clothing Scraper"
    MAX_LINE_LENGTH = 80
    BORDER_CHAR = "*"

    def display_program_name(self) -> None:
        """
        Displays the name of the program at the top of the terminal screen.
        The text is centered and surrounded by a border on top and bottom.
        """
        self._draw_centered_message(self.PROGRAM_NAME)

    def _draw_centered_message(self, message: str) -> None:
        """
        Private method to print a centered message with borders.

        Args:
            message (str): The message to be centered and bordered.
        """
        border = self.BORDER_CHAR * self.MAX_LINE_LENGTH
        centered_message = message.center(self.MAX_LINE_LENGTH - 2)
        print(f"{border}\n{self.BORDER_CHAR}{centered_message}{self.BORDER_CHAR}\n{border}")

    def format_long_message(self, message: str) -> str:
        """
        Format a long message to fit within the maximum line length.
        Also adds the necessary border characters to the message.

        Args:
            message (str): The message to format.

        Returns:
            str: The formatted message.
        """
        lines = []
        while len(message) > self.MAX_LINE_LENGTH - 4:  # Adjust for borders
            index = message.rfind(" ", 0, self.MAX_LINE_LENGTH - 4)
            if index == -1:
                index = self.MAX_LINE_LENGTH - 4
            lines.append(
                (
                    f"{self.BORDER_CHAR} "
                    f"{message[:index].ljust(self.MAX_LINE_LENGTH - 4)} "
                    f"{self.BORDER_CHAR}"
                )
            )
            message = message[index:].lstrip()

        lines.append(
            f"{self.BORDER_CHAR} {message.ljust(self.MAX_LINE_LENGTH - 4)} {self.BORDER_CHAR}"
        )

        return "\n".join(lines)

    def _draw_border(self) -> None:
        """
        Draws a horizontal border based on the max line length.
        """
        print(self.BORDER_CHAR * self.MAX_LINE_LENGTH)

    def display_output(self, message: str) -> None:
        """
        Display formatted output to the user via the command line.
        This method handles long messages, fitting them to the screen width.

        Args:
            message (str): The message to display.
        """
        print(self.format_long_message(message))

    def display_information_list(self, information_list: list) -> None:
        """
        Display a list of information in a formatted table-like structure with borders
        and within the maximum line length defined by the UI.

        Args:
            information_list (list): A list of strings to display.
        """
        if not information_list:
            return

        max_content_length = self.MAX_LINE_LENGTH - 4  # Adjust for borders

        # Calculate the actual max length of the content in each line (consider word wrapping)
        formatted_lines = []
        for item in information_list:
            while len(item) > max_content_length:
                index = item.rfind(" ", 0, max_content_length)
                if index == -1:
                    index = max_content_length
                formatted_lines.append(
                    f"{self.BORDER_CHAR} "
                    f"{item[:index].ljust(max_content_length)} "
                    f"{self.BORDER_CHAR}"
                )
                item = item[index:].lstrip()
            formatted_lines.append(
                f"{self.BORDER_CHAR} {item.ljust(max_content_length)} {self.BORDER_CHAR}"
            )

        # Draw the top border
        self._draw_border()

        # Print each formatted line
        for line in formatted_lines:
            print(line)

        # Draw the bottom border
        self._draw_border()

    def get_input(self, prompt: str) -> str:
        """
        Get input from the user via the command line.

        Args:
            prompt (str): The prompt message to display.

        Returns:
            str: The user's input from the command line.
        """
        return input(prompt)

    def clear_screen(self) -> None:
        """
        Clear the terminal screen. The command used depends on the operating system:
        - For Windows, it uses the 'cls' command.
        - For Unix-like systems (Linux, macOS), it uses the 'clear' command.
        """
        os.system("cls" if platform.system() == "Windows" else "clear")
