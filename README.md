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

本リポジトリは、Koemotion/Koeiromapを利用される方に向けたツールや情報等を提供します。

## 準備
本リポジトリに含まれるコードは、以下の環境で動作を確認しています。
- Python 3.8.13
- Ubuntu 22.04 (on WSL2)

Koemotion用のツールを利用する場合には、ffmpegが必要となります。例えばUbuntuの場合、以下のコマンドでインストールしてください。
```
sudo apt install ffmpeg
```

Pythonの仮想環境を用意し、有効化しておきます。
```
python3 -m venv venv
source venv/bin/activate
```
以降は各ツールごとのREADMEに従って、必要なライブラリをインストールしてください。

## ツール
- [`tools/facemotion`](./tools/facemotion) にKoemotionから返ってきた音声および顔のキーポイントを動画化するスクリプトを提供しています。



