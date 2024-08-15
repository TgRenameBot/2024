import os

class Config(object):
    # get a token from @BotFather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    # Banned Unwanted Members..
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    # the download location, where the HTTP Server runs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    # set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 3600
    # watermark file
    DEF_WATER_MARK_FILE = ""
    # Update channel for Force Subscribe
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "MyTestBotZ")
    AUTH_CHANNEL = "@myTestbotz"
    #database url
    DB_URI = os.environ.get("DATABASE_URL", "")
    #Time Limit
    try:
        TIME_GAP = int(os.environ.get("TIME_GAP", "")) if os.environ.get("TIME_GAP", "") else None
    except:
        TIME_GAP = None
        logger.warning("Give the timegap in seconds. Dont use letters 😑")
    TIME_GAP_STORE = {}


