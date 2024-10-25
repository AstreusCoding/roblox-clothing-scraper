"""
This module defines the `Interface` abstract base class
and its command-line implementation, `CLIInterface`.
"""

from abc import ABC, abstractmethod


class Interface(ABC):
    """
    Abstract base class for different types of interfaces. All interfaces must implement
    methods to get input from the user and display output.
    """

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """
        Get input from the user.

        Args:
            prompt (str): The prompt message to display to the user.

        Returns:
            str: The user's input.
        """

    @abstractmethod
    def display_output(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message (str): The message to display.
        """
