# upwork_discord_bot

The Upwork Discord Bot is a Python-based bot that fetches and displays job listings from Upwork in a Discord server. It uses the `discord.py` library for interacting with Discord's API, and the `selenium` library to scrape job listings from Upwork's website.

## Prerequisites

Before running the bot, make sure you have the following installed:

- Python 3.x
- [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html#installing)
- [selenium](https://selenium-python.readthedocs.io/installation.html)
- [geckodriver](https://github.com/mozilla/geckodriver/releases) (required by Selenium for Firefox)

## Setup

1. Clone this repository to your local machine.
2. Create a `.env` file in the same directory as your script (`bot.py`) and add your Discord Bot token:
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```
# Bot Commands

## Fetch Jobs

Use the **!fetch_jobs** command to manually fetch and display job listings from Upwork in the Discord server.

## Selenium

Use the **!selenium** command to run Selenium to fetch and display job listings asynchronously using separate threads.

## Automated Job Fetching

The bot is also configured to automatically fetch job listings and send them to a specified Discord channel at regular intervals. You can adjust the interval duration by modifying the fetch_and_send_jobs coroutine in the bot.py script.

# Contributing

Feel free to contribute to this project by submitting pull requests or reporting issues on the GitHub repository.

# Disclaimer

This project is intended for educational and personal use only. Be sure to follow Upwork's terms of use and scraping guidelines.
License

This project is licensed under the MIT License.
