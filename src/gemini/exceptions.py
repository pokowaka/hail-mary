class AiResponseError(Exception):
    """Raised when the AI model's response is invalid or cannot be parsed."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

    def __str__(self):
        if self.details:
            return f"{super().__str__()} Details: {self.details}"
        return super().__str__()
