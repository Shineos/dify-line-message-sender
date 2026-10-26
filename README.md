<div align="center">

  [![README in English](https://img.shields.io/badge/English-06C755)](./README.md)
  [![日本語のREADME](https://img.shields.io/badge/日本語-d9d9d9)](./readme/README_ja.md)

</div>

# LINE Message Sender

A [Dify](https://dify.ai) plugin that sends push and broadcast messages to LINE users and groups, right from your Dify workflows — via the [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/overview/).

> Note: This is a community plugin by [shineos](https://shineos.com). It is not an official LINE product.

## Features

- **Send Push Message** — send a text message to a specific LINE user, group, or room
- **Send Broadcast Message** — send a text message to all friends of your LINE Official Account
- **Get User Profile** — fetch a LINE user's display name, user ID, picture URL, and status message
- **Get Bot Info** — fetch your LINE Official Account's information (useful as a connection test)

## Typical use cases

- Notify workflow results (daily reports, monitoring alerts, form submissions) to LINE users or groups
- Broadcast announcements from a Dify workflow on a schedule
- Look up a LINE user's profile before composing a personalized reply

## Setup

1. Create a **Messaging API channel** on the [LINE Developers Console](https://developers.line.biz/console/) (requires a LINE Official Account; the free plan works).
2. On the channel's **Messaging API** tab, issue a **long-lived channel access token**.
3. In Dify, install this plugin, open **Tools → LINE Message Sender**, and paste the token as *Channel access token*.
4. Use **Get Bot Info** once to confirm the connection works.

Notes:

- Push messages only reach users who are friends of the bot, and group/room IDs only work while the bot is in that group/room.
- Recipient IDs look like `U...` (user), `C...` (group), `R...` (room).
- Broadcast messages count toward your LINE plan's monthly message quota.

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

## Troubleshooting

**Tools fail with empty credentials (`keys=[]`) in an imported workflow** — a Dify-side quirk on self-hosted 1.16–1.18: tool nodes whose `provider_type` is `"plugin"` skip credential loading. If you import a workflow via DSL, make sure the tool nodes use `provider_type: "builtin"` (the UI writes this value automatically when you add nodes by hand). Credential setup itself is unchanged: authorize once in **Tools → LINE Message Sender**.

## Privacy

See [PRIVACY.md](PRIVACY.md). The plugin stores your channel access token in your Dify workspace and sends requests only to `api.line.me`.

## Questions

- Maintainer: shineos — https://shineos.com
- Source code: https://github.com/Shineos/dify-line-message-sender
- LINE Messaging API reference: https://developers.line.biz/en/reference/messaging-api/
