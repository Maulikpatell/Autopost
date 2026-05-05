from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from bot.config import API_ID, API_HASH

sessions = {}


async def start_session(event):
    user_id = event.sender_id
    sessions[user_id] = {"step": "phone"}

    await event.reply(
        "📱 Send your phone number (with country code)\nExample: +919876543210"
    )


async def handle_session(event):
    user_id = event.sender_id

    if user_id not in sessions:
        return

    data = sessions[user_id]
    text = event.raw_text.strip()

    try:
        # STEP 1 → PHONE
        if data["step"] == "phone":
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()

            await client.send_code_request(text)

            data.update({
                "client": client,
                "phone": text,
                "step": "code"
            })

            await event.reply("📩 Enter OTP code")

        # STEP 2 → CODE
        elif data["step"] == "code":
            client = data["client"]

            try:
                await client.sign_in(
                    phone=data["phone"],
                    code=text
                )

            except SessionPasswordNeededError:
                data["step"] = "password"
                await event.reply("🔐 Enter your 2FA password")
                return

            string = client.session.save()
            await client.disconnect()

            sessions.pop(user_id, None)

            await event.reply(f"✅ SESSION STRING:\n\n`{string}`")

        # STEP 3 → PASSWORD
        elif data["step"] == "password":
            client = data["client"]

            await client.sign_in(password=text)

            string = client.session.save()
            await client.disconnect()

            sessions.pop(user_id, None)

            await event.reply(f"✅ SESSION STRING:\n\n`{string}`")

    except Exception as e:
        sessions.pop(user_id, None)
        await event.reply(f"❌ Error: {e}")
