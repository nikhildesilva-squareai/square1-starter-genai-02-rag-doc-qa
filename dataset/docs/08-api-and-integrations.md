# API and Integrations

The Nimbus Notes REST API lets you create, read, and update notes programmatically.
Generate a personal API token in **Settings → Developer**. Authenticate by sending
the token in an `Authorization: Bearer <token>` header.

The API is rate-limited to 120 requests per minute per token. Native integrations
are available for Slack (post a note to a channel) and Zapier (trigger workflows
when a note is created). Webhooks can notify your own server when a note in a
shared notebook changes.
