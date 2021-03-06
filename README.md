# What does it do?
[![PyPI](https://img.shields.io/pypi/v/praw?color=orange&label=praw&style=flat-square)](https://pypi.org/project/praw/)

It's a simple Reddit bot, it comments on every new submission. If the comment gets to a certain score or below, a message linking to the post will be sent to the ModMail. The bot will constantly check the new queue and the list of comments. all comments are saved to a local database.

# How do I install it?
1) Download this repo.
2) Install the requirements by running `pip3 install -r requirements.txt`.
3) Add your account details in `praw.ini`.
4) Run it by using `python3 bot.py` (it will automatically create a database).

# ⚠ WARNING ⚠

Please be careful if you use this on a live SubReddit. The bot is experimental and may not work fully. **Try on a test SubReddit first.**
