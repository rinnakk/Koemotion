# Facemotion
## 準備
事前に作成したPythonの仮想環境を有効化しておきます。（新たに仮想環境を作成しても構いません）
```
source ../../venv/bin/activate
```
必要なライブラリをインストールします。
```
pip install -r requirements.txt
```

## キーポイントの動画化
Koemotionから返ってきた音声および顔のキーポイントが以下のように配置されているとします。
```
- sample.wav  # 他のフォーマット (mp3, opus) でも問題ありません
- sample.json
```
`visualize.py`を実行することで、顔のキーポイントをフレームごとに描画して動画化し、音声と結合します。実行時には必要なライブラリをインストールしたPython仮想環境を事前に有効化してください。
```
python visualize.py -i sample.json -a sample.wav -o sample.mp4
```