# Grokログ抽出ツール

Grokからダウンロードしたログデータから会話部分のみを抽出し、
読みやすいHTML形式に変換するPythonスクリプトです。

HTMLファイルは、各チャットごとに「<会話タイトル>.html」という形式で生成されます。
HTMLに加えて、txt形式およびjson形式でも出力されます。

---

## 準備

### Grokログのダウンロード

- https://accounts.x.ai/data からGrokのログデータをダウンロードし、解凍してください。

⚠ 注意
「prod-grok-backend.json」にはチャット履歴やタイムスタンプなどの個人情報が含まれます。
このファイルをリポジトリにコミットすることは絶対に避けてください。
.gitignore に追加することを強く推奨します。

---

### Pythonのインストール

- https://www.python.org/ からPython 3.8以上をインストールしてください
- 外部ライブラリは不要で、標準ライブラリのみで動作します

---

### スクリプトの配置

- grok_log_export.py を prod-grok-backend.json と同じフォルダに配置してください

⚠ 注意
- 保存時に「ファイルの種類」を「すべてのファイル」に設定してください
- 拡張子が .py になっていることを確認してください

---

## 実行方法

### ダブルクリックで実行

- Pythonファイルをダブルクリックすることで実行できます

---

### ターミナル（コマンドライン）で実行

#### パスの確認

例（Windows）:

```
C:\Users\ユーザー名\Downloads...\export_data\英数字羅列\
```

---

#### ターミナルを開く

- Windows: 検索バーで cmd と入力 → Enter
- macOS/Linux: ターミナルを起動

---

#### コマンドを実行

Windows:

```
cd "C:\Users\ユーザー名\Downloads\解凍したログのフォルダ\ttl\30d\export_data\英数字の羅列\"
python grok_log_export.py
```

macOS/Linux:

```
cd /Users/ユーザー名/Downloads/解凍したログのフォルダ/ttl/30d/export_data/英数字の羅列/
python3 grok_log_export.py
```

⚠ 注意
環境によっては python ではなく python3 を使用してください

---

## 出力内容

会話タイトルごとにフォルダが作成され、以下の構造で出力されます。

```
/[Conversation_Title]/
  ├── html/
  │    ├── Conversation_Title.html   # 全期間ログ
  │    ├── YYYY-MM.html              # 月別ログ
  │    └── index.html                # 月別・全期間へのリンク
  ├── json/
  │    ├── Conversation_Title.json
  │    └── YYYY-MM.json
  └── txt/
       ├── Conversation_Title.txt
       └── YYYY-MM.txt
```

---

## 注意事項

- human / assistant の1対1の会話ペアのみを抽出対象としています
- タイムスタンプは日本時間（JST）として表示されます
（Grokの仕様上、厳密なタイムゾーンは保証されません）

---

## 非対応機能

- チャット内の添付ファイル（画像・ファイル）
- 再生成による分岐ログ
- バックエンドでの検索結果
- エージェント機能（複数人格による生成など）
- 画像・動画生成時のログ

---

## 補足

- ダブルクリックで実行した場合、処理完了後にウィンドウが閉じることがあります

---

## 免責事項

本スクリプトの利用は自己責任でお願いします。
本スクリプトの使用によって発生したいかなる損害についても、製作者は責任を負いません。
