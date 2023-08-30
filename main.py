import praw
import os
import telegram
import requests
import re
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# Initialize Telegram Bot API client
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

# In-memory storage for sent posts
sent_posts = {}


def sanitize_markdown(text):
    # Remove Markdown formatting characters (e.g., **, __, etc.)
    sanitized_text = re.sub(r"[*_~`]", "", text)
    return sanitized_text


def send_post_to_telegram(submission, chat_id):
    title = submission.title
    selftext = submission.selftext
    url = submission.url

    sanitized_title = sanitize_markdown(title)
    sanitized_selftext = sanitize_markdown(selftext)

    text = f"{sanitized_title}\n{sanitized_selftext}"

    if url.endswith((".jpg", ".png", ".gif")):
        image_url = url
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open("image.jpg", "wb") as file:
                file.write(response.content)
            bot.send_photo(chat_id=chat_id, photo=open("image.jpg", "rb"), caption=text,
                           parse_mode=telegram.ParseMode.MARKDOWN)
            os.remove("image.jpg")


def check_new_posts(context):
    for chat_id in sent_posts.keys():
        subreddit = reddit.subreddit(os.getenv("REDDIT_SUBREDDIT"))
        for submission in subreddit.new(limit=100):
            if submission.id not in sent_posts[chat_id]:
                send_post_to_telegram(submission, chat_id)
                sent_posts[chat_id].append(submission.id)


def start(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    bot_name = os.getenv("TELEGRAM_BOT_NAME")
    subreddit_name = os.getenv("REDDIT_SUBREDDIT")
    welcome_message = f"Hello {user.first_name}!\n\nI'm {bot_name}, your MemesBot. I will send you new memes from the subreddit {subreddit_name}. Get ready to enjoy some relatable content!"
    update.message.reply_text(welcome_message)

    # Send the 100 newest posts immediately on /start
    subreddit = reddit.subreddit(os.getenv("REDDIT_SUBREDDIT"))
    sent_posts[chat_id] = []  # Initialize an empty list for this user
    for submission in subreddit.new(limit=100):
        send_post_to_telegram(submission, chat_id)
        sent_posts[chat_id].append(submission.id)

    # Schedule a job to check for new posts periodically
    context.job_queue.run_repeating(check_new_posts, interval=600, first=0)


def main():
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
