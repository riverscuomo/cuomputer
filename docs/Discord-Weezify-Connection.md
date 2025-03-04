# Discord to Weezify Account Connection Documentation

## Overview

This document provides information about connecting Discord accounts to Weezify ([weezify.web.app](https://weezify.web.app)) accounts. It focuses on processes, troubleshooting, and administration rather than technical implementation details which can be found in code comments.

## Connection Process for Users

1. **Join the Discord Server**: New members automatically receive the "Visitor" role.

2. **Receive DM with Snowflake ID**: The bot sends a DM containing:
   - Instructions link
   - The user's Discord snowflake ID

3. **Enter Snowflake ID on Weezify**: User must add their Discord snowflake ID to their profile on [weezify.web.app](https://weezify.web.app).

4. **Connect in Discord**: User goes to the #connect-to-mrn channel and types their exact Weezify username (case-sensitive).

5. **Verification & Role Assignment**: Upon successful verification, the user receives the "Neighbor" role and appropriate bundle roles.

## Known Issues for Users

### DM Privacy Settings

**Issue**: Users with restrictive DM privacy settings won't receive their snowflake ID message.

**Solution**: 
- Temporarily enable "Allow direct messages from server members" in Discord privacy settings
- Or find their Discord ID manually: In any Discord server, click the Users icon, find their username, right-click, and select "Copy ID"

### Channel Access Issues

**Issue**: Some roles may not have access to the #connect-to-mrn channel.

**Solution**: Contact an administrator to check channel permissions.

### Connection "Limbo" State

**Issue**: Users who receive the Neighbor role before connecting may have incorrect role assignments.

**Solution**: Contact an administrator who can check your connection status and reset roles if needed.

## Administrative Actions

### Manual Connection Override

If a user can't connect through the normal process:

1. Retrieve their Discord snowflake ID
2. Find their Weezify account in Firestore
3. Update their `discordId` field with their snowflake ID
4. Set `discordConnected` to true
5. Assign the Neighbor role manually

### Troubleshooting User Access

When users report connection issues:

1. Check their DM privacy settings
2. Verify they have access to the #connect-to-mrn channel
3. Check channel permissions for their current roles
4. Look for their account in Firestore to verify connection status

## Channel Instructions Message

The following message should be pinned in the #connect-to-mrn channel:

```
1. Make sure you have created a Weezify account at https://www.weezify.web.app
2. Go to your profile screen at https://www.weezify.web.app
3. Enter your discord snowflake id*
4. Come back to this channel
5. Send a message that consists only of your MRN username (case-sensitive)
6. The bot will reply with a message confirming connection

*HOW TO FIND YOUR DISCORD SNOWFLAKE ID: 
First, try typing your MRN username (case-sensitive) in this channel. The bot will reply with your discord snowflake ID.
OR
In any Discord server, click the Users icon in the upper right corner. Find your username in the list of users, right click it, and then select Copy ID.
```

## Discord Permission Structure

### Discord Roles

- **Visitor**: New members (based on configured waiting period)
- **Neighbor**: Members who have successfully connected their Discord to Weezify
- **Bundle-specific roles**: Based on Weezify bundles owned (White, Blue-Pinkerton, etc.)

### Channel Permissions

- The #connect-to-mrn channel should be accessible to all new members
- Once connected (with Neighbor role), the channel may be hidden
- Some special roles may need explicit permissions to see the connect channel

## Monitoring and Maintenance

- Review Heroku logs for connection errors
- Periodically audit channel permissions
- Verify new users are connecting successfully
- Ensure welcome DMs are being received

## Reference Information

### Key Configuration

- `neighbor_role_waiting_period` in config.py controls how long users remain as Visitors before becoming Neighbors
  - "instant": 0 hours (immediate promotion)
  - "delayed24": 24 hours (1 day waiting period)
