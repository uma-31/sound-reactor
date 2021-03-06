# Sound Reactor
登録した音声をボイスチャットで再生できるDiscord BOT


## 開発を始める
Linux環境の場合，次のコマンドで依存関係にあるライブラリを取得してください．

```shell
$ apt install libffi-dev libnacl-dev python3-dev ffmpeg
```

以下のコマンドをプロジェクトディレクトリ直下で実行し，
仮想環境を作成します．

※ Pythonは3.9以上を使用してください．

```shell
$ git config --local core.hooksPath .githooks
$ pip install --upgrade pip
$ pip install pipenv
$ pipenv sync --dev
```

### 起動設定
Sound Reactorは，
`config.json`で設定されたトークンか，
環境変数`SOUND_REACTOR_TOKEN`が設定されている場合はその値を使用してBOTを稼働させます．

誤ってトークン情報をpushするのを防ぐため，
環境変数を設定することをおすすめします．

### スクリプト
Pipfileに登録されているスクリプトは次の通りです．

| スクリプト名 | 説明 |
| :--- | :--- |
| start | ボットを立ち上げる |
| format | autopep8による自動フォーマットを行う |
| lint | flake8によるチェックを行う |

スクリプトを実行するには，プロジェクトディレクトリ直下で以下のコマンドを実行します．

```
$ pipenv run <スクリプト名>
```

## docstring
[Numpy形式](https://numpydoc.readthedocs.io/en/latest/format.html)を採用します．

## コミットメッセージ
`prefix: message`の形式に従います．

有効なPrefixは以下の通りです．

| Prefix | 説明 |
| :--- | :--- |
| chore | 本体の機能に関わらない変更 |
| docs | ドキュメントの変更 |
| feat | 新しい機能の追加 |
| fix | バグの修正 |
| perf | パフォーマンス改善 |
| refactor | リファクタリング |
| test | テストの変更 |
