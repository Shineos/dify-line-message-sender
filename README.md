# LINE Message Sender

**Author:** shineos
**Version:** 0.2.0
**Type:** tool

A [Dify](https://dify.ai) plugin that sends push and broadcast messages to LINE users and groups, right from your Dify workflows — via the [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/overview/).

> Note: This is a community plugin by [shineos](https://shineos.com). It is not an official LINE product.

## Overview

The plugin gives your workflows four tools around one credential — a single **channel access token** covers everything:

- **Send Push Message** — send a text message to a specific LINE user, group, or room
- **Send Broadcast Message** — send a text message to all friends of your LINE Official Account
- **Get User Profile** — fetch a LINE user's display name, user ID, picture URL, and status message
- **Get Bot Info** — fetch your LINE Official Account's information (useful as a connection test)

Typical use cases:

- Notify workflow results (daily reports, monitoring alerts, form submissions) to LINE users or groups
- Broadcast announcements from a Dify workflow on a schedule
- Look up a LINE user's profile before composing a personalized reply

## Tools

### Send Push Message

Sends a text message to one recipient. The bot must be a friend of the user, or a member of the group/room.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `to` | string | Yes | Recipient LINE ID: user (`U...`), group (`C...`), or room (`R...`) |
| `message_text` | string | Yes | Text to send (up to 5,000 characters) |
| `notification_disabled` | boolean | No | If true, the message arrives without a push notification |

Returns JSON: `{"status": "sent", "to": "...", "request_id": "..."}`

### Send Broadcast Message

Sends a text message to **all friends** of the LINE Official Account. No recipient parameter.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message_text` | string | Yes | Text to broadcast (up to 5,000 characters) |
| `notification_disabled` | boolean | No | If true, messages arrive without push notifications |

Returns JSON: `{"status": "sent", "scope": "all_friends", "request_id": "..."}`

### Get User Profile

Fetches a user's profile. The user must be a friend of the bot.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | Yes | LINE user ID starting with `U` |

Returns the LINE profile JSON: `displayName`, `userId`, `pictureUrl`, `statusMessage`.

### Get Bot Info

Fetches the official account's own information — no parameters. Use it once after setup to confirm the credential works.

Returns JSON: `userId` (the bot's own user ID, usable as a webhook filter), `basicId` (its LINE ID, e.g. `@abc123`), `displayName`, `chatMode`, `marked`.

## Setup

### Step 1 — Create a Messaging API channel

1. Go to the [LINE Developers Console](https://developers.line.biz/console/) and sign in with your LINE account.
2. Create a **provider** (your company or product name), or pick an existing one.
3. Under the provider, create a channel of type **Messaging API**. This requires a LINE Official Account — the free plan works.

![LINE Developers Console: create a Messaging API channel](_assets/setup-1-create-channel.png)

### Step 2 — Issue a channel access token (long-lived)

1. Open the channel you created and go to the **Messaging API** tab.
2. Scroll to **Channel access token (long-lived)** and click **Issue**.
3. Copy the generated token. Use this long-lived token — not the short-lived one under the Basic settings tab.

![LINE Developers Console: issue a long-lived channel access token](_assets/setup-2-issue-token.png)

### Step 3 — Install the plugin in Dify

Install **LINE Message Sender** by shineos from **Dify Marketplace** (search for "LINE"), or upload the `.difypkg` file from the [GitHub releases](https://github.com/Shineos/dify-line-message-sender/releases) if your Dify cannot reach the Marketplace.

![Dify Marketplace: install the plugin](_assets/setup-3-install-plugin.png)

### Step 4 — Authorize the provider

1. In Dify, open **Tools → LINE Message Sender → Authorize**.
2. Paste the channel access token from Step 2 and save.

![Dify: authorize LINE Message Sender with the channel access token](_assets/setup-4-authorize.png)

### Step 5 — Test the connection

Run **Get Bot Info** once. If you see your account's `basicId` and `displayName` in the JSON response, the connection works.

![Dify: run Get Bot Info and confirm the JSON response](_assets/setup-5-bot-info.png)

## Usage

Add a tool node to any workflow or chatflow:

1. Add the **LINE Message Sender** tool node and pick one of the four tools.
2. Fill in the parameters — e.g. for a push message, set `to` to the recipient's user ID and `message_text` to the body.
3. Run the workflow. On success the node outputs JSON with a `request_id` from LINE.

A typical pattern is a scheduled workflow (cron trigger → fetch data / LLM summary → **Send Push Message**), or a chatflow that ends by notifying the user's LINE account.

### Finding recipient IDs

The plugin sends by ID, so you need the recipient's LINE user ID:

- **User IDs (`U...`)** come from webhook payloads — e.g. a `follow` event when someone adds your bot as a friend, or `message` events. Inspect them with any webhook receiver, including a Dify endpoint plugin.
- **Group/room IDs (`C...` / `R...`)** likewise come from webhook events while the bot is in that group or room.
- Your own bot's ID is available any time via **Get Bot Info** (`userId` field).

## Notes

- Push messages only reach users who are friends of the bot, and group/room IDs only work while the bot is in that group/room.
- Broadcast messages count toward your LINE plan's monthly message quota.
- The plugin only sends text messages; image/flex templates are not supported yet.
- The plugin makes outbound connections only to `api.line.me`.

## Anti-abuse and acceptable use

This plugin sends real messages to real people. When you use it, you are the sender of record, so:

- **Send only to people who opted in.** Push messages can only reach users who are friends of your bot, and group/room sends only work while the bot is a member — LINE enforces this. Do not try to work around it.
- **Broadcast responsibly.** Each broadcast consumes your LINE plan's monthly message quota and reaches every friend of the account. You are responsible for complying with the [LINE Official Account terms and guidelines](https://terms2.line.me/official_account_api_terms/) and any laws that apply to your messaging, including Japan's Act on Regulation of Transmission of Specified Electronic Mail for commercial messages.
- **Use `notification_disabled` sparingly.** Silent delivery is meant for low-priority operational traffic (e.g. log digests), not for hiding unwanted bulk messages.
- **Keep sensitive personal data out of message text.** Messages remain in the recipient's LINE chat history, so avoid credentials and sensitive personal information in the body.
- **Design workflows with rate limits in mind.** Avoid loops that push one message per item to the same recipient; batch or summarize instead. LINE enforces API rate limits, and abusive patterns can get your channel throttled or suspended by LINE.

## Build and test

Python 3.12 is required. Install runtime and test dependencies, then run the offline test suite:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

To build an installable package with the Dify plugin CLI, run this from the parent directory:

```sh
dify plugin package ./line-message-sender
```

The package contains the plugin runtime and documentation. Tests and development scripts are excluded by `.difyignore`.

## Privacy

See [PRIVACY.md](PRIVACY.md). The plugin stores your channel access token in your Dify workspace and sends requests only to `api.line.me`.

## Questions

- Maintainer: shineos — https://shineos.com
- Source code: https://github.com/Shineos/dify-line-message-sender
- LINE Messaging API reference: https://developers.line.biz/en/reference/messaging-api/
