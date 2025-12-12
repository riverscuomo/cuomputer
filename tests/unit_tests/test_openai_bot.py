"""Tests for openai_bot.py message handling."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from bot.on_message.bots.openai_bot import OpenAIBot, PromptParams


class MockMember:
    """Mock Discord Member (has nick attribute)."""
    def __init__(self, name: str, nick: str = None):
        self.name = name
        self.nick = nick


class MockUser:
    """Mock Discord User (no nick attribute, like cross-posted message authors)."""
    def __init__(self, name: str):
        self.name = name
        # Note: no nick attribute - this is intentional


class MockMessage:
    """Mock Discord message for testing."""
    def __init__(self, content: str, author_name: str = "TestUser", author_has_nick: bool = True):
        self.content = content
        if author_has_nick:
            self.author = MockMember(author_name)
        else:
            self.author = MockUser(author_name)
        self.attachments = []


class MockChannel:
    """Mock Discord channel with configurable message history."""
    def __init__(self, messages: list[MockMessage]):
        self._messages = messages

    def history(self, limit: int, oldest_first: bool):
        return MockAsyncIterator(self._messages[:limit])


class MockAsyncIterator:
    """Async iterator for mock channel history."""
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self._items):
            raise StopAsyncIteration
        item = self._items[self._index]
        self._index += 1
        return item


@pytest.mark.asyncio
async def test_create_message_prompt_skips_empty_content():
    """Verify that messages with empty content (like server announcements) are skipped."""
    messages = [
        MockMessage("Hello everyone!", "User1"),
        MockMessage("", "ServerAnnouncement"),  # Empty content (announcement)
        MockMessage("How's it going?", "User2"),
        MockMessage("   ", "AnotherAnnouncement"),  # Whitespace-only content
        MockMessage("Great day!", "User3"),
    ]
    
    channel = MockChannel(messages)
    prompt_params = PromptParams(
        system_prompt="Test system prompt",
        user_prompt="Test user prompt",
        user_name="TestUser",
        channel=channel,
        max_tokens=100,
        lookback_count=10
    )
    
    result = await OpenAIBot._create_message_prompt(prompt_params)
    
    # Should have: system message + 3 valid user messages + final user prompt = 5 total
    assert len(result) == 5
    
    # First message should be system prompt
    assert result[0]["role"] == "system"
    assert result[0]["content"] == "Test system prompt"
    
    # User messages should only include non-empty content (in oldest_first=False order, then reversed)
    user_messages = [m for m in result if m["role"] == "user"]
    assert len(user_messages) == 4  # 3 from history + 1 user_prompt
    
    # Verify no empty content messages made it through
    for msg in user_messages:
        content = msg["content"]
        # Content should not be just "AuthorName: " with nothing after
        assert not content.endswith(": ")
        assert content.strip() != ""


@pytest.mark.asyncio
async def test_create_message_prompt_handles_all_empty_messages():
    """Verify behavior when all history messages have empty content."""
    messages = [
        MockMessage("", "Announcement1"),
        MockMessage("   ", "Announcement2"),
    ]
    
    channel = MockChannel(messages)
    prompt_params = PromptParams(
        system_prompt="Test system prompt",
        user_prompt="Test user prompt",
        user_name="TestUser",
        channel=channel,
        max_tokens=100,
        lookback_count=10
    )
    
    result = await OpenAIBot._create_message_prompt(prompt_params)
    
    # Should have: system message + user_prompt only (no history messages)
    assert len(result) == 2
    assert result[0]["role"] == "system"
    assert result[1]["role"] == "user"
    assert result[1]["content"] == "Test user prompt"


@pytest.mark.asyncio
async def test_create_message_prompt_handles_user_without_nick():
    """Verify that User objects (without nick attribute) don't crash - bug #97 fix."""
    messages = [
        MockMessage("Hello!", "RegularMember", author_has_nick=True),
        MockMessage("Server announcement", "ServerBot", author_has_nick=False),  # User object, no nick
        MockMessage("Another message", "AnotherMember", author_has_nick=True),
    ]
    
    channel = MockChannel(messages)
    prompt_params = PromptParams(
        system_prompt="Test system prompt",
        user_prompt="Test user prompt",
        user_name="TestUser",
        channel=channel,
        max_tokens=100,
        lookback_count=10
    )
    
    # Should not raise AttributeError: 'User' object has no attribute 'nick'
    result = await OpenAIBot._create_message_prompt(prompt_params)
    
    # All 3 messages should be included (none are empty)
    user_messages = [m for m in result if m["role"] == "user"]
    assert len(user_messages) == 4  # 3 from history + 1 user_prompt
    
    # Verify the User object message used author.name as fallback
    assert any("ServerBot:" in m["content"] for m in user_messages)
