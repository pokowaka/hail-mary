import base64
import json
import logging
import os
import socket
import urllib.error
import urllib.request


class GeminiAuthenticator:
    """Handles authentication for the Gemini API."""

    def __init__(
        self,
        service_account_email="build-runner@emulator-builds.iam.gserviceaccount.com",
    ):
        self.service_account_email = service_account_email

    def get_credentials(self, model):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return {
                "api_key": api_key,
                "endpoint": f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
                "auth_mode": "API Key",
                "headers": {"Content-Type": "application/json"},
            }

        raise RuntimeError(
            "Failed to configure Gemini client with any authentication method."
        )
