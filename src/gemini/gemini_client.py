import asyncio
import json
import logging
import urllib.error
import urllib.request

from .gemini_auth import GeminiAuthenticator


class GeminiClient:
    """A client for the Gemini API."""

    def __init__(
        self,
        model="gemini-2.5-flash",
        service_account_email="build-runner@emulator-builds.iam.gserviceaccount.com",
    ):
        self.model = model
        authenticator = GeminiAuthenticator(service_account_email)
        credentials = authenticator.get_credentials(self.model)

        self.api_key = credentials["api_key"]
        self.headers = credentials["headers"]
        self.endpoint = credentials["endpoint"]
        self.auth_mode = credentials["auth_mode"]

    def _prepare_request_body(self, prompt):
        return {"contents": [{"parts": [{"text": prompt}]}]}

    def generate_content(self, prompt):
        body = self._prepare_request_body(prompt)
        json_data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint, data=json_data, headers=self.headers, method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body)
        except Exception as e:
            logging.error(f"Request failed: {e}")
            raise

    def parse_response(self, response_json):
        extracted_text = []
        try:
            candidates = response_json.get("candidates", [])
            for candidate in candidates:
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    if "text" in part:
                        extracted_text.append(part["text"])
        except (AttributeError, KeyError) as e:
            raise ValueError("Invalid response JSON format.") from e
        return extracted_text

    async def get_generated_text(self, prompt):
        loop = asyncio.get_event_loop()
        raw_response = await loop.run_in_executor(None, self.generate_content, prompt)
        text_list = self.parse_response(raw_response)
        return "".join(text_list)
