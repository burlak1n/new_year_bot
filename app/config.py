import os

import dotenv

dotenv.load_dotenv()


# токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# список id админов
admin_ids_str = os.getenv("ADMIN_IDS")
ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()] if admin_ids_str else []

# соль для генерации номера письма
salt = os.getenv("SALT")

# шаблон ссылки
link_template = "https://t.me/test_burlak1n_bot?start={encrypted}"

# ключ для шифрования данных
encryption_key = bytes.fromhex(os.getenv("ENCRYPTION_KEY"))
if len(encryption_key) != 32:
    raise ValueError(f"ENCRYPTION_KEY должен быть 64 hex символа (32 байта), получено {len(encryption_key)} байт")
