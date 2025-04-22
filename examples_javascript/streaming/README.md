# JavaScript Streaming Sample

このサンプルでは、Koemotion API から stream を取得し、Web ブラウザーで再生することを目的とします。
UI の実装に HTML、javascript、API の実装に nodejs、express を利用しています。
このため、本サンプルは本リポジトリが提供する Python ライブラリをインストールせずに利用することができます。
UI の実装に関しては `public/` フォルダー内を参照ください。
API の実装に関しては `main.js` を参照ください。

## ローカル環境でのサンプルの実行手順

このサンプルは nodejs を利用して作成されています。nodejs をインストールしていただく必要があります。

1. `main.js:l6` の `apiKey` 変数にご自身の API key を設定してください。
2. このサンプルのルートディレクトリーに移動し以下を実行します。
3. `npm ci`
4. `npm run start`
5. サービスが立ち上がるので、`http://localhost:3000` をブラウザーで開きます。
6. テキストボックスに話させたい文字を入力し、Submit ボタンを押すと音声が再生されます。

## 任意のサービス内での実装方法

任意の環境における実装の手順は以下のようになります。

1. AudioContext を、例えばユーザーのクリックイベントのようなユーザージェスチャーの後に作成します。
   これはブラウザーの仕様であり、スピーカーから音声を再生する際には必ず必要となる処理です。
   Developer tools の Console パネル内で `The AudioContext was not allowed to start. It must be resumed (or created) after a user gesture on the page` のような Warning が表示されている場合、ユーザーアクションの後に AudioContext が作成できていないことがわかります。ご注意ください。

   本サンプルでは話させたい文章を入力し、Submit ボタンを押すことで再生される UI となっているため、ユーザージェスチャーを自然と得ることができます。
   状況によっては、「このページでは音声が再生されます。」といったポップアップを表示し、「続ける」を押させるなどの工夫が必要となります。

2. ご自身の API service 内で Koemotion API を呼び出す proxy のような動きをする endpoint を作成します。
   本サンプルでは `https://api.rinna.co.jp/koemotion/infer` の proxy となるサービスを作成頂くことになります。実装にあたっての注意点は以下の通りです。

   - rinna 提供の API key をクライアントアプリ内で利用しない。必ずご自身の API service 内でのみ利用すること。
     サービスを利用するユーザーが API key を取得できてしまうと、そのユーザーが API key を所持するアカウントとして rinna 社の API を呼び出すことができるようになってしまいます。
   - サービスの endpoint 内で、Koemotion API の Response body を chunk 単位で read し、read 出来たものから順次 response の stream に書きだすこと。
     全てを読み込んだ後に response に書きだすような処理を書いてしまうと、stream の生成速度の恩恵を受けることができなくなります。

3. `public/script.js` 内の `playAudioStreamByWavStream` 関数または同等の処理を行う関数をクライアントコード内に配置し、ステップ 2 で作成いただいた endpoint の response body を渡すことで、音声が再生されます。
