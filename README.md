# AniBmBot.exe

Welcome to AniBmBot.exe! Developed by [Itamar](https://github.com/CMOSfail), this bot fetches and sends memes directly from Reddit to Telegram. It's designed to be versatile and can adapt to any subreddit of your choice.

## Getting Started

### Prerequisites
1. [Python 3.11.5](https://www.python.org/downloads/release/python-3115/)

### Installation and Setup

1. Clone or download this repository.
2. Extract the contents into your desired folder.
3. Rename `.env.example` to `.env`.
4. Fill in the `.env` file with all of your API keys.
   - [Reddit App Creation](https://www.reddit.com/prefs/apps)
   - [Telegram Bot Creation](https://core.telegram.org/bots#6-botfather)
5. Execute `run.bat`.
6. Enjoy the bot!

## How It Works

At its core, the bot utilizes the [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/) to fetch memes from your chosen subreddit and the [Telegram API](https://core.telegram.org/bots/api) to send them directly to your Telegram chat. 

1. Initialize Reddit and Telegram clients.
2. Check the 100 newest posts from the chosen subreddit.
3. Send each post directly to the user on Telegram.
4. Periodically check for new posts and send them.

## Contributing

Any contributions you make are **greatly appreciated**. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Developer: [Itamar](https://github.com/CMOSfail)

Project Link: [https://github.com/CMOSfail/AniBmBot.exe](https://github.com/CMOSfail/AniBmBot.exe)
