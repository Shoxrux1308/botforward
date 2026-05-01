from dotenv import load_dotenv
import os
from telethon import TelegramClient, events
import re

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

client = TelegramClient("session", api_id, api_hash)


# ESKI YOZUV
# =========================
OLD_TEXT = "👉 @Uzbekiston24 - телеграм каналига обуна бўлинг!"

# =========================
# YANGI YOZUV
# =========================
NEW_TEXT = """




Дўстлик бозори каналига қўшилинг: 👇
@dostlik_bozor2

Реклама бўйича:
@shohrux_1308
@azizjon_dev
"""

# =========================
# TEXT TOZALASH
# =========================
def clean_text(text):

    if not text:
        return ""

    # Kerakli joyni almashtirish
    text = text.replace(OLD_TEXT, NEW_TEXT)

    # Linklarni olib tashlash
    text = re.sub(r'http\S+', '', text)

    # Ortiqcha bo‘sh joylarni tozalash
    text = re.sub(r'\n+', '\n', text)

    return text.strip()


# ====================================================
# ALBUM (BIR NECHTA RASM/VIDEO/FILE)
# ====================================================
@client.on(events.Album(chats=SOURCE_CHANNEL))
async def album_handler(event):

    files = []
    caption = ""

    for msg in event.messages:

        # Caption olish
        if msg.message:
            caption = clean_text(msg.message)

        # Har qanday media
        if msg.media:
            files.append(msg.media)

    # Yuborish
    await client.send_file(
        TARGET_CHANNEL,
        file=files,
        caption=caption
    )

    print("✅ Album yuborildi")


# ====================================================
# ODDIY POSTLAR
# ====================================================
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def new_message_handler(event):

    # Agar album bo‘lsa skip
    if event.message.grouped_id:
        return

    msg = event.message

    text = clean_text(msg.message or "")

    # =========================
    # MEDIA BO‘LSA
    # =========================
    if msg.media:

        await client.send_file(
            TARGET_CHANNEL,
            file=msg.media,
            caption=text
        )

        print("✅ Media yuborildi")

    # =========================
    # ODDIY TEXT
    # =========================
    else:

        await client.send_message(
            TARGET_CHANNEL,
            text
        )

        print("✅ Text yuborildi")


# ====================================================
# START
# ====================================================
print("🚀 Bot ishga tushdi...")

client.start()

client.run_until_disconnected()