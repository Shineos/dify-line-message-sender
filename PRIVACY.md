# Privacy

## What this plugin stores

- The **channel access token** you enter when configuring the plugin. It is stored inside your Dify workspace (Dify's credential storage) and is used only to authenticate requests to the LINE Messaging API.

## What this plugin sends

- The plugin sends HTTPS requests **only** to `api.line.me`, the official LINE Messaging API endpoint:
  - `POST /v2/bot/message/push`
  - `POST /v2/bot/message/broadcast`
  - `GET /v2/bot/profile/{userId}`
  - `GET /v2/bot/info`
- The content of these requests is limited to the data you provide in the workflow (recipient IDs, message text) and the channel access token.

## What this plugin does not do

- It does not collect, log, or transmit any data to the plugin developer (shineos) or to any third party other than LINE.
- It does not store message contents or recipient IDs beyond the lifetime of the tool invocation.
- It contains no telemetry or analytics.

## Third parties

- LINE Corporation receives your requests as part of the LINE Messaging API. Their handling is governed by [LINE's terms and privacy policy](https://terms2.line.me/official_account_api_terms/).

## Contact

- shineos — https://shineos.com
