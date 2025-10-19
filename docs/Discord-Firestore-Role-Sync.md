# Discord ⇄ Firestore Role Synchronization

This note explains how Discord role changes propagate into Firestore (and related side effects) inside the `cuomputer` bot. It’s meant to give future contributors a quick map before touching the flow.

## Event Entry Point
- Discord emits `on_member_update(before, after)` for every role change.
- The handler lives in `bot/on_member_update/on_member_update.py`.
- Members listed in `config.members_to_skip` are ignored up front.

## Finding Role Deltas
- The handler compares `before.roles` vs. `after.roles` and builds two lists:
  - `added_roles`: roles present after the change but not before.
  - `removed_roles`: roles present before the change but not after.
- The code now loops each list so multiple simultaneous role edits are handled correctly (older versions only processed the first difference).

## Firestore User Lookup
- `get_firestore_user_by_id` (`bot/scripts/add_roles.py`) queries the `users` collection for a matching `discordId`.
- The helper normalizes the Firestore document to include defaults (email, bundle IDs, badges, etc.), which downstream logic relies on.
- Firestore access is provided by the singleton client in `bot/db/fbdb.py`, initialized via `firebase_admin` Application Default credentials.

## Role Metadata
- Google Sheet data (tab `Roles`) is loaded once per process via `load_roles_sheet` (`bot/setup/services/roles_sheet.py`).
- On each update we build a dictionary keyed by role name so we can enrich notifications and perform Drive access control.
- The sheet records optional fields like `description`, `type`, `folder_id`, and `google_drive_role`.

## Badge Updates & Notifications
For each role added:
1. Append the role name to the user’s `badges` array using `firestore.ArrayUnion`.
2. If the user has a valid email and the metadata lists a Drive folder:
   - Grant access through the Google Drive API (role defaults to `commenter` unless overridden).
3. Trigger platform-specific extras (e.g., Android/iPhone tester sheet updates).
4. DM the member with the standard “You’ve been given…” message, plus:
   - Role description (if present).
   - `config.service_message` when the role type matches service/role-assigner categories.

For each role removed:
1. Remove the badge via `firestore.ArrayRemove`.
2. Revoke Drive access when metadata includes a `folder_id` (tester removal helpers are present but currently commented out).
3. DM messaging for removals is disabled in the current implementation but easy to re-enable if desired.

## Legacy Behavior & Guarantees
- The Firestore badge write has existed for a long time; existing role holders should already have matching badges.
- The 2025-02 update simply extends the handler to cover multi-role edits and fixes metadata loading so Drive/DM enrichment works reliably.
- Manual edits directly in Firestore are overwritten only when a Discord role change occurs—routine role grants/removals stay as the source of truth.

## Implementation Checklist
- Ensure `.env` or runtime env vars supply `GOOGLE_CLOUD_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS`, and `GOOGLE_DRIVE_CREDFILE`; otherwise Firestore/Drive calls will fail.
- Keep the Roles sheet in sync with new Discord roles so badge syncing and messaging stay coherent.
- When running locally, simulate role changes by toggling roles on a test user and verifying:
  - Firestore `badges` updates spread across all roles changed in one action.
  - Drive permissions add/remove as expected.
  - DM copy looks correct for service roles.

