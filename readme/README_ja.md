**Languages**: [English](../README.md) | 日本語（本ファイル）

# LINEメッセージ送信（LINE Message Sender）

[Dify](https://dify.ai) のワークフローから、[LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/overview/) を使ってLINEユーザー・グループへメッセージを送信するDifyプラグインです。

> ※株式会社シャイオス（[shineos](https://shineos.com)）が提供するコミュニティプラグインです。LINE株式会社の公式プラグインではありません。

## 提供するツール

- **メッセージ送信（個別）** — 特定のLINEユーザー・グループ・トークルームへテキストを送信（プッシュメッセージ）
- **メッセージ送信（全員）** — LINE公式アカウントの友だち全員へ一斉送信（ブロードキャスト）
- **ユーザープロフィール取得** — 表示名・ユーザーID・プロフィール画像URL・ステータスメッセージを取得
- **ボット情報取得** — 公式アカウントの情報を取得（接続テストに利用できます）

## 典型的な使い方

- 日次レポートや監視アラート、フォーム受付通知をワークフローからLINEへ通知
- スケジュール実行（トリガー）でキャンペーン告知を友だち全員に一斉配信
- 個別返信の前にユーザープロフィールを取得してパーソナライズ

## セットアップ手順

1. [LINE Developersコンソール](https://developers.line.biz/console/) で **Messaging APIチャネル** を作成します（LINE公式アカウントが必要。無料プランで開始できます）。
2. チャネルの「**Messaging API**」タブで**長期のチャネルアクセストークン**を発行します。
3. Difyで本プラグインをインストールし、「ツール → LINE Message Sender」でトークンを登録します。
4. 「ボット情報取得」を一度実行して、接続を確認します。

注意:

- プッシュメッセージは、ボットの**友だちになっているユーザー**、またはボットが**参加しているグループ・トークルーム**にのみ届きます
- 宛先IDの先頭文字: `U`=ユーザー / `C`=グループ / `R`=トークルーム
- ブロードキャストの送信数はLINEプランの月間無料枠にカウントされます

## プライバシー

[PRIVACY.md](PRIVACY.md) を参照してください。チャネルアクセストークンはDifyワークスペース内に保存され、プラグインは `api.line.me` にのみリクエストを送信します。

## 提供元

- 株式会社シャイオス（shineos）— https://shineos.com
- ソースコード: https://github.com/Shineos/dify-line-message-sender
- LINE Messaging API リファレンス: https://developers.line.biz/ja/reference/messaging-api/
