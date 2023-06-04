class FileDoesNotExistError(Exception):
    """Exception raised when a file does not exist."""

    def __init__(self, file_path: str):
        """Initialise the exception.

        Args:
            file_path (Path): The path to the file that does not exist.
        """
        super().__init__(f"!SKIPPING TASK! File '{file_path}' does not exist.")
        self.file_path = file_path
