<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/Koemotion_logo_1980_600_dark.png">
    <source media="(prefers-color-scheme: light)" srcset="./assets/Koemotion_logo_1980_600_light.png">
    <img alt="Koemotion" src="./assets/Koemotion_logo_1980_600_light.png" width="396" height="120" style="max-width: 100%;">
  </picture>
  <br/>
</p>

<h3 align="center">
    <a href="https://koemotion.rinna.co.jp/">https://koemotion.rinna.co.jp/</a>
</h3>
<br/>

本リポジトリは、Koemotionを利用される方に向けたPythonライブラリと、関連する情報等を提供します。

## 準備

> [!TIP]
> 以下ではPythonライブラリのインストール方法、使い方、利用例等を説明しています。
> もしもKoemotionから得られる音声をWebブラウザで再生したいとお考えの場合、Pythonライブラリは不要です。
> 代わりに [`examples_javascript/`](./examples_javascript/) 以下にあるJavaScriptサンプルコードをご確認ください。


本リポジトリに含まれるコードは、以下の環境で動作を確認しています。
- Python 3.8.13
- Windows 11 / macOS Sonoma 14.3.1 / Ubuntu 22.04 (on WSL2)

### 関連パッケージのインストール
本ライブラリは`pyaudio`ライブラリを利用するため、事前に`portaudio`のインストールが必要になります。
```sh
# macOS
brew install portaudio
# Ubuntu
sudo apt install portaudio19-dev
```
Facemotionに関連したツールを利用する場合には、`ffmpeg`が必要となります。
```sh
# macOS
brew install ffmpeg
# Ubuntu
sudo apt install ffmpeg
```

### Pythonライブラリのインストール
以下のコマンドでPythonライブラリをインストールできます。事前にPython仮想環境を用意し、有効化しておくことをおすすめします。
```sh
# python3 -m venv venv
# source venv/bin/activate
pip install git+https://github.com/rinnakk/Koemotion
```

以下のPythonスクリプトやコマンドラインツールを利用してAPIコールを行う場合、環境変数`KOEMOTION_API_KEY`にAPIキーを登録してください。Koemotionへの登録方法は[docs/subscription.md](./docs/subscription.md)を参照ください。
```sh
export KOEMOTION_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 使い方
`Koemotion`クラスのインスタンスを作成します。ここで環境変数`KOEMOTION_API_KEY`に登録したAPIキーが内部的に読み込まれます。
```Python
from koemotion import Koemotion

client = Koemotion()
```
環境変数の登録がうまくいかない場合など、明示的にAPIキーを指定したい場合は以下のように指定することもできます。
```Python
client = Koemotion(api_key="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
```

### 通常の音声合成
合成用のパラメータを定義し、`request()`メソッドに与えます。`request()`メソッドの呼び出しによりAPIがコールされ、**Koemotion Light/Standard/Businessプランでは課金が発生**します。料金の詳細については[こちら](https://koemotion.rinna.co.jp/?section=pricing)をご確認ください。
```
params = {
  "text": "今日はいい天気ですね",
  "speaker_x": 2.0,
  "speaker_y": 3.0,
}
response = client.request(params)
```
`response`は`KoemotionJsonResponse`オブジェクトで返されます。結果をファイルに保存する場合は以下のように`save_json()`または`save_audio()`メソッドを呼び出します。
```Python
response.save_json("result.json")
response.save_audio("result.mp3")
```

### ストリーミング音声合成
Koemotion Standard/Businessプランに登録している場合、ストリーミング音声合成が利用できます。パラメータに`"output_format": "wav"`と`"streaming": True`を指定し、同様に`request()`メソッドをコールします。
`"trim_leading_silence": True`の指定は任意ですが、冒頭の無音区間を短縮することができるため、より高速な音声応答が必要なケース等で有効です。
```Python
params = {
  "text": "今日はいい天気ですね",
  "speaker_x": 2.0,
  "speaker_y": 3.0,
  "output_format": "wav",
  "streaming": True,
  "trim_leading_silence": True,
}
response = client.request(params)
```
`response`は`KoemotionStreamingResponse`オブジェクトとなります。

ストリーミング音声合成の利点は「音声全体の合成が完了する前に音声のダウンロードが開始される」点にあります。この利点を活かす一つの機能として、`stream_audio()`メソッドを呼ぶことでローカルデバイスで音声を逐次再生することができます。
```Python
response.stream_audio()
```
より高度な処理を行いたい場合には、`response.response.iter_content()`から実際に受け取った音声データのバイナリ列にアクセスすることも可能です。
ストリーミング音声合成の場合にも`save_audio()`メソッドから音声を保存することができますが、**このメソッドは音声全体のダウンロードを待つ（ストリーミングの利点は失われる）** ことにご注意ください。
```Python
response.save_audio("result_streaming.wav")  # wait until the entire audio is downloaded
```

## CLIツール
Pythonライブラリのインストール、および環境変数`KOEMOTION_API_KEY`の登録ができている場合、以下のようにコマンドラインから直接APIをコールすることができます。結果はデフォルトで`result.json`に保存されます。
```sh
koemotion-request -d "{\"text\": \"こんにちは\"}"
```
`-a/--output-audio`を指定することで、音声をファイルに書き出すことができます。
```sh
koemotion-request -d "{\"text\": \"こんにちは\"}" -a result.mp3 
```
ストリーミング音声合成を利用する場合（Koemotion Standard/Businessプランへの登録が必要です）は、jsonファイルは保存されず、代わりにデフォルトで`result_streaming.wav`に音声が保存されます。`--autoplay`を指定することで、音声全体のダウンロードを待たずにローカルの音声デバイスで再生を始めることができます。
```sh
koemotion-request -d "{\"text\": \"こんにちは\", \"output_format\": \"wav\", \"streaming\": true, \"trim_leading_silence\": true}" --autoplay
```


## 利用例
- [`examples/facemotion`](./examples/facemotion): Koemotionから返ってきた音声および顔のキーポイントを動画化する
- [`examples/streaming/streaming_demo.py`](./examples/streaming/streaming_demo.py): ストリーミング音声合成をPythonから実行する
- [`examples/streaming/realtime_chat_demo.py`](./examples/streaming/realtime_chat_demo.py): GPT-4o APIとKoemotionを利用して、リアルタイムな音声応答を得る（OpenAIのAPIキーの登録、および`openai`ライブラリのインストールが必要です）
- [`examples_javascript/streaming`](./examples_javascript/streaming): Koemotionからストリーミングされた音声をWebブラウザーで再生する (Python環境は不要です)
