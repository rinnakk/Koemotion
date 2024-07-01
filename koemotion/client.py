import os
from typing import Optional

import httpx

from .response import KoemotionJsonResponse, KoemotionStreamingResponse


class Koemotion:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        if api_key is None:
            api_key = os.environ.get("KOEMOTION_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key must be set either by passing api_key or setting the KOEMOTION_API_KEY environment variable."
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("KOEMOTION_BASE_URL")
        if base_url is None:
            base_url = "https://api.rinna.co.jp/koemotion/infer"
        self.base_url = base_url

        self.client = httpx.Client()

    def __del__(self):
        self.client.close()

    def request(self, params: dict, headers: dict = None):
        """
        Args:
            params (dict): Request body.
            header (dict): Additional request header. Necessary headers are included by default.
        Returns:
            KoemotionJsonResponse or KoemotionStreamingResponse: Response object.
        """
        headers_ = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-key": self.api_key,
        }
        if headers is not None:
            headers_.update(headers)

        stream = params.get("streaming", False)

        try:
            req = self.client.build_request(
                "POST", self.base_url, headers=headers_, json=params
            )
            response = self.client.send(req, stream=stream)
            response.raise_for_status()
        except Exception as e:
            if "response" in locals():
                response.read()
                print("Error: ", response.text)
                response.close()
            raise e

        if params.get("streaming", False):
            return KoemotionStreamingResponse(params, response)
        else:
            return KoemotionJsonResponse(params, response)
