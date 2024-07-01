import base64
import os

from .streaming import save_audio, stream_audio


class KoemotionResponse:
    def __init__(self, params, response):
        """
        Args:
            params (dict): Request body.
            response (httpx.Response): Response object.
        """
        super().__init__()
        self.params = params
        self.response = response

    def __del__(self):
        self.response.close()


class KoemotionJsonResponse(KoemotionResponse):
    def __init__(self, params, response):
        """
        Args:
            params (dict): Request body.
            response (httpx.Response): Response object.
        """
        super().__init__(params, response)
        self.data = response.json()
        self.audio = self.data["audio"].split(",")[1]
        self.phonemes = self.data["phonemes"]
        self.seed = self.data["seed"]
        self.style = self.data.get("style", None)

    def save_audio(self, output_path, quiet=False):
        """
        Save audio to file.
        Args:
            output_path (str): Path to save the audio file.
            quiet (bool): Suppress log if True.
        """
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(self.audio))

        if not quiet:
            print("Audio saved to", output_path)

    def save_json(self, output_path, quiet=False):
        """
        Save JSON to file.
        Args:
            output_path (str): Path to save the JSON file.
            quiet (bool): Suppress log if True.
        """
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(self.response.text)

        if not quiet:
            print("JSON saved to", output_path)


class KoemotionStreamingResponse(KoemotionResponse):
    def __init__(self, params, response):
        """
        Args:
            params (dict): Request body.
            response (httpx.Response): Response object.
        """
        super().__init__(params, response)
        self.audio_data = None

    def save_audio(self, output_path="", quiet=False):
        """
        Save the audio stream from the response object to a WAV file.
        Note that this function waits for the entire audio stream to be downloaded before saving.

        Args:
            output_path (str): Path to save the audio file.
            quiet (bool): Suppress log if True.
        """
        if not output_path:
            output_path = "result_streaming.wav"

        if self.audio_data:
            save_audio(self.audio_data, output_path)
        else:
            save_audio(self.response.content, output_path)

        if not quiet:
            print("Audio saved to", output_path)

    def stream_audio(self, chunk_size=1024):
        """
        Play the audio stream from the response object.

        Args:
            chunk_size (int): Size of the audio chunk to stream.
        """
        self.audio_data = stream_audio(self.response, chunk_size)
