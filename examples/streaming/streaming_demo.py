from koemotion import Koemotion

koemotion_client = Koemotion()

koemotion_params = {
    "speaker_x": 2.0,
    "speaker_y": 3.0,
    "output_format": "wav",
    "streaming": True,
}

text = input("読み上げたいテキストを入力してください: ")
koemotion_params["text"] = text
response = koemotion_client.request(koemotion_params)
response.stream_audio()
response.save_audio("result_streaming.wav")
