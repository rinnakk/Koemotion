# Facemotion

## キーポイントの動画化
Koemotionから返ってきた音声および顔のキーポイントが以下のように配置されているとします。
```
- sample.wav  # 他のフォーマット (mp3, opus) でも問題ありません
- sample.json
```
`koemotion-visualize`コマンドを実行することで、顔のキーポイントをフレームごとに描画して動画化し、音声と結合します。
実行時には必要なライブラリをインストールしたPython仮想環境を事前に有効化してください。
```
koemotion-visualize -i sample.json -a sample.wav -o sample.mp4 (--quiet) (--overwrite)
```