import os
from dotenv import load_dotenv

load_dotenv()

encryption_key = b"your-32-byte-key-here!!!!!!!!!!!"  # 32 bytes для ChaCha20
link_template = "https://t.me/test_burlak1n_bot?start={encrypted}"

ADMIN_IDS = []

BOT_TOKEN = os.getenv("BOT_TOKEN")