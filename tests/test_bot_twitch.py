import pytest

from bots.twitch import TwitchBot


@pytest.fixture
def default_bot():
    return TwitchBot()


def test_exists(default_bot):
    assert isinstance(default_bot, TwitchBot)
