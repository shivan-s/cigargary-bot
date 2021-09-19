import pytest

from twitch.bot import Bot


@pytest.fixture
def default_bot():
    return Bot()


def test_exists(default_bot):
    assert isinstance(default_bot, Bot)
