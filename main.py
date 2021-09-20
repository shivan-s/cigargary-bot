#!python3.8
# main.py - main python file to run

from bots.twitch import TwitchBot


def main():
    twitch_bot = TwitchBot()
    twitch_bot.run()


if __name__ == "__main__":
    main()
