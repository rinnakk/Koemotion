from time import perf_counter

from openai import OpenAI

from koemotion import Koemotion

openai_client = OpenAI()
koemotion_client = Koemotion()

messages = [
    {
        "role": "system",
        "content": "以降のユーザ発話に対して気の効いたリアクションや質問を一言で作成してください．絵文字や記号は含めてはいけません",
    }
]
koemotion_params = {
    "speaker_x": 2.0,
    "speaker_y": 3.0,
    "output_format": "wav",
    "streaming": True,
}

while True:
    messages.append({"role": "user", "content": input("User: ")})
    start_time_openai = perf_counter()
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=32,
    )
    end_time_openai = perf_counter()
    content = response.choices[0].message.content
    print("System:", content)
    print(f"OpenAI API response time: {end_time_openai - start_time_openai:.3f} sec")
    messages.append({"role": "system", "content": content})

    koemotion_params["text"] = content
    start_time_koemotion = perf_counter()
    response = koemotion_client.request(koemotion_params)
    end_time_koemotion = perf_counter()
    print(
        f"Koemotion API response time: {end_time_koemotion - start_time_koemotion:.3f} sec"
    )
    response.stream_audio()
    response.save_audio(f"wav/{content}.wav", quiet=True)
