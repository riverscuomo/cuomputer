# Agents

This document captures the automated agents and companion services that power the `cuomputer` Discord bot. Each entry references the key module, explains how the agent is triggered, and lists any noteworthy dependencies so new contributors can reason about impacts before making changes.

## On-Message Agents

### OpenAIBot (Rivers Persona)

- **Purpose**: Primary conversational agent that replies as Rivers Cuomo, optionally generating voice audio for RC-talk.
- **Triggers / Inputs**: Instantiated in `bot/setup/bots.py` and invoked by `bot/on_message/respond.py` whenever message heuristics allow a response (channel gating, `user_score`, random die roll, mentions). Uses `CustomMessage` envelopes with `gpt_system` seeds defined per channel.
- **Outputs**: Posts text replies via `discord.TextChannel.send`; in `channels["rctalk"]` it also streams an ElevenLabs MP3 into voice chat through `reply_with_voice`.
- **Owner**: Rivers Cuomo (`config.rivers_id`).
- **Notes**: Implementation lives in `bot/on_message/bots/openai_bot.py`. Uses OpenAI `gpt-4o-mini` with a function call hook that queries `WeezerpediaAPI` for context, applies a response lock (`asyncio.Lock`) to avoid double replies, and enforces a ten-response-per-day voice cap per user. Slash-command summarizers reuse its `fetch_openai_completion`.

### Channel Persona Handlers

- **Purpose**: Adjust Rivers’s persona and decide whether OpenAIBot should answer in specific text channels (artists, coach, sarah, vangie, etc.).
- **Triggers / Inputs**: Called from `bot/on_message/respond.py`; each handler in `bot/on_message/bots/response_handlers.py` evaluates `CustomMessage` fields (channel ID, `user_score`, newbie flag, die roll, mentions).
- **Outputs**: Mutates `message.gpt_system` with channel-specific directives before delegating to `openai_bot.post_ai_response`.
- **Owner**: Rivers Cuomo / server staff.
- **Notes**: Conversation frequency profiles (`ConversationStyle`) control how chatty Rivers should be. Update these when introducing new channels or personas to keep alignment with moderation goals.

### RolesBot

- **Purpose**: Answers “how do I get X role?” questions in the Q&A channel by reading the shared Google Sheet.
- **Triggers / Inputs**: `post_roles_response` in `bot/on_message/bots/rolesbot.py` is invoked from `respond` when the message lives in `channels["qna"]` and mentions both “role” and timing keywords.
- **Outputs**: Sends a templated text reply outlining requirements and links the full role sheet.
- **Owner**: Rivers Cuomo.
- **Notes**: Depends on `bot/setup/services/roles_sheet.load_roles_sheet()`, which caches Google Sheet data for the process lifetime. Remember to refresh the cache if editing the sheet schema.

### Q&A Default Responder

- **Purpose**: Provides fallback instructions when no specialist bot answers a support question.
- **Triggers / Inputs**: `post_qna_default_response` is the last handler inside the Q&A branch of `respond`.
- **Outputs**: Posts a mult-line message redirecting users to channel-specific entry points.
- **Owner**: Rivers Cuomo.
- **Notes**: Implementation at `bot/on_message/bots/qna_default.py`. Update messaging when server onboarding flows change.

### Google Dialogflow Intent Bot (disabled)

- **Purpose**: Legacy Dialogflow intent handler for canned responses.
- **Triggers / Inputs**: `post_google_response` in `bot/on_message/bots/googlebot.py`; call is commented out in `respond`, so it currently never runs.
- **Outputs**: Would send Dialogflow fulfillment text back to Discord.
- **Owner**: Rivers Cuomo (historical).
- **Notes**: Uses `bot.setup.services.google_services.init_dialogflow`. Restore the call in `respond` if the Dialogflow agent becomes active again; otherwise consider pruning.

### KnowledgeBot (deprecated)

- **Purpose**: Older Dialogflow Knowledge Base integration.
- **Triggers / Inputs**: `post_google_knowledge_response` in `bot/on_message/bots/knowledgebot.py`; marked with `@DeprecationWarning` and unused.
- **Outputs**: Would send trimmed knowledge-base answers.
- **Owner**: Rivers Cuomo (historical).
- **Notes**: Keep around only if you plan to revive the knowledge connector; the module logs to stdout and assumes environment Dialogflow credentials.

## Membership & Role Agents

### Onboarding Flow (`on_member_join`)

- **Purpose**: Welcomes new members and kicks off the Discord↔Weezify linking process.
- **Triggers / Inputs**: Discord `on_member_join` event handled in `bot/on_member_join/on_member_join.py`.
- **Outputs**: Assigns the “Visitor” role, posts a welcome in `channels["welcome"]`, and DMs detailed connection instructions including the member’s snowflake ID.
- **Owner**: Rivers Cuomo.
- **Notes**: Depends on `fetch_roles` to find the Visitor role and `name_contains_profanity` to block problematic usernames. Users with DM restrictions will miss the instructions—responders should know to resend manually.

### Role Sync & Drive Access (`on_member_update`)

- **Purpose**: Keeps Firestore badges and Google Drive folder permissions in sync with Discord roles.
- **Triggers / Inputs**: Discord `on_member_update` event wired in `bot/on_member_update/on_member_update.py`; reacts to role adds/removes.
- **Outputs**: Updates Firestore `users.badges`, grants or revokes Google Drive access via the Drive API, and optionally DMs members with additional info.
- **Owner**: Rivers Cuomo.
- **Notes**: Skips IDs in `config.members_to_skip`. Pulls role metadata from the Roles sheet, so failures there bubble up. The Drive operations require service-account credentials loaded in `config.py`.

### MRN Connector

- **Purpose**: Confirms a member’s Weezify username and marks their account as connected.
- **Triggers / Inputs**: `bot/scripts/connect_to_mrn.connect_to_mrn` runs inside `on_message` when someone posts in `channels["connect"]` with a short message.
- **Outputs**: Sends success/error responses in-channel and flips the Firestore `discordConnected` flag on success.
- **Owner**: Rivers Cuomo.
- **Notes**: Expects users to have stored their Discord snowflake ID on Weezify; emits detailed error guidance when the IDs do not match.

## Slash Command Agents

### `/weezerpedia`

- **Purpose**: Fetches Weezerpedia knowledge and optional infobox art.
- **Triggers / Inputs**: Slash command registered in `bot/slash_commands/commands.py`; takes a search term and uses `WeezerpediaAPI.get_search_result_knowledge`.
- **Outputs**: Sends markdown-formatted context and (when available) an infobox image attachment.
- **Owner**: Rivers Cuomo.
- **Notes**: Conversions depend on `requests` calls to the public Weezerpedia API plus `InfoboxGenerator` for artwork. Be mindful of rate limits.

### `/riverpedia`

- **Purpose**: Surfaces curated Riverpedia entries.
- **Triggers / Inputs**: Slash command calling `RiverpediaAPI.get_wiki_response`.
- **Outputs**: Posts the selected entry text plus a URL.
- **Owner**: Rivers Cuomo.
- **Notes**: `RiverpediaAPI` loads entries from Firestore (`bot/db/fetch_data.fetch_entries`). Responses are filtered to avoid recently used entries.

### `/summarize`

- **Purpose**: Summarizes recent channel activity for supporters.
- **Triggers / Inputs**: Slash command guarded by `is_supporter()` in `commands.py`; builds a `PromptParams` request and reuses `openai_bot.fetch_openai_completion`.
- **Outputs**: Posts a formatted summary to the current channel.
- **Owner**: Rivers Cuomo.
- **Notes**: Defaults to the last 15 messages (`DEFAULT_MESSAGE_LOOKBACK_COUNT`) but accepts a `count` argument. Failures are silently ignored via `contextlib.suppress`.

### `/summarize_and_advise`

- **Purpose**: Private briefing for Rivers—summarize a channel, then DM actionable advice.
- **Triggers / Inputs**: Command limited to `config.rivers_id`. Runs two sequential OpenAIBot prompts (summary, then advisor).
- **Outputs**: Posts channel summary publicly and sends advice via DM.
- **Owner**: Rivers Cuomo.
- **Notes**: Relies on successful DM delivery; check Rivers’s privacy settings if DMs fail.

### `/servertime`

- **Purpose**: Shares how long a user has been in the server.
- **Triggers / Inputs**: Slash command in `commands.py`; no special permissions.
- **Outputs**: Ephemeral message stating days since `interaction.user.joined_at`.
- **Owner**: Rivers Cuomo.
- **Notes**: Uses `discord.utils.utcnow()`; returns zero if `joined_at` is missing.

## Supporting Services

### WeezerpediaAPI

- **Purpose**: Wraps Weezerpedia search and page conversion.
- **Triggers / Inputs**: Called by OpenAIBot function-calls and the `/weezerpedia` command.
- **Outputs**: Returns markdown-formatted content plus optional Discord `File` objects with generated infoboxes.
- **Owner**: Rivers Cuomo.
- **Notes**: Implementation in `bot/on_message/bots/weezerpedia.py`. Uses `requests` and `wiki_to_markdown`; ensure credentials allow outbound HTTP when deploying.

### RiverpediaAPI

- **Purpose**: Serves curated Riverpedia facts for commands (and historically message responses).
- **Triggers / Inputs**: Instantiated at startup in `bot/setup/bots.py` and used by the `/riverpedia` command.
- **Outputs**: Titles, URLs, and text snippets pulled from Firestore.
- **Owner**: Rivers Cuomo.
- **Notes**: Maintains an in-memory cache of entries with a “recently used” cooldown. Random mode is available via `pick_random_entry`.

### InfoboxGenerator

- **Purpose**: Renders Weezerpedia infobox data into shareable images.
- **Triggers / Inputs**: Created by `WeezerpediaAPI` when a page contains an `{{Infobox}}` template.
- **Outputs**: Generates a PIL image streamed back to Discord via `discord.File`.
- **Owner**: Rivers Cuomo.
- **Notes**: Fonts are loaded from `data/fonts`. Bundles album-specific coloring and layout logic—update here if adding new infobox types.
