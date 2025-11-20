import json
import urllib.request
import urllib.parse
import os
from typing import Dict

from dotenv import load_dotenv

class OpenFigiClient:
    def __init__(self):
        load_dotenv()
        self.OPENFIGI_API_KEY = os.environ.get("OPENFIGI_API_KEY", None)
        self.OPENFIGI_BASE_URL = "https://api.openfigi.com"

    def api_call(
        self,
        path: str,
        data: Dict | None = None,
        method: str = "POST",
    ) -> Dict:
        """
        Make an api call to `api.openfigi.com`.

        Args:
            path (str): API endpoint, for example "search"
            method (str, optional): HTTP request method. Defaults to "POST".
            data (dict | None, optional): HTTP request data. Defaults to None.

        Returns:
            JsonType: Response of the api call parsed as a JSON object
        """

        headers = {"Content-Type": "application/json"}
        if self.OPENFIGI_API_KEY:
            headers |= {"X-OPENFIGI-APIKEY": self.OPENFIGI_API_KEY}

        request = urllib.request.Request(
            url=urllib.parse.urljoin(self.OPENFIGI_BASE_URL, path),
            data=data and bytes(json.dumps(data), encoding="utf-8"),
            headers=headers,
            method=method,
        )

        with urllib.request.urlopen(request) as response:
            json_response_as_string = response.read().decode("utf-8")
            json_obj = json.loads(json_response_as_string)
            return json_obj


    def search_request(self, request: Dict):
        search_response = self.api_call("/v3/search", request)
        return json.dumps(search_response)


    def mapping_request(self, request: Dict):
        mapping_response = self.api_call("/v3/mapping", request)
        return json.dumps(mapping_response)
