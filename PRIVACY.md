# Privacy

This document describes how the LINE Message Sender plugin handles your data.

## What this plugin stores

- The **channel access token** you enter when configuring the plugin. It is stored inside your Dify workspace (Dify's credential storage), used only to authenticate requests to the LINE Messaging API, and removed when you de-authorize the provider or uninstall the plugin.

## Message content handling

Each tool invocation handles two pieces of user data: the **recipient ID(s)** and the **message text**.

- Both exist only as tool invocation parameters, held in the plugin process's **memory** while the tool runs.
- They are forwarded over **HTTPS (TLS)** to `api.line.me` within the same invocation, and to nowhere else.
- When the invocation ends, both are **discarded**. The plugin writes nothing to disk, keeps no cache, and writes no application logs.
- Message content is never used for analytics, model training, or any other purpose by the plugin or by shineos.

## What this plugin does not collect

- It does not store recipient IDs, message contents, or send statistics beyond the lifetime of a single tool invocation.
- It does not record workflow inputs or outputs.
- It contains no telemetry, analytics, or crash reporting.

## Developer access

- shineos, the plugin developer, has **no access** to data inside your Dify workspace. The plugin only makes outbound requests to LINE and registers no inbound endpoints, so no external party — including shineos — can connect to it or pull data from it.

## Data retention

- **Message text and recipient IDs:** no retention — discarded when the tool invocation ends.
- **Channel access token:** retained by Dify's credential storage until you remove or replace it in the plugin's authorization settings.

## Third parties

- LINE Corporation receives your requests as part of the LINE Messaging API. Their handling is governed by [LINE's terms and privacy policy](https://terms2.line.me/official_account_api_terms/).
- No other third party receives any data from the plugin.

## Contact

- shineos — https://shineos.com
