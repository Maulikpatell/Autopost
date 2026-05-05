

---

# 🚀 Telegram Auto Content Loop Bot

A powerful Telegram automation system that continuously reposts content from source channels to multiple destination channels with smart scheduling, looping, and content modification.

---

## ✨ Features

- 🔁 Infinite Loop Posting System (no reset, no duplicates)
- 📡 Multi Source → Multi Destination Mapping
- ⏱️ Smart Daily Post Distribution
- 🕒 Custom Posting Hours (per channel)
- 🧠 Auto Indexing of New Content
- ✂️ Telegram Link Cleaner / Replacer
- 🏷️ Footer Injection System
- 👥 Multi-Admin Control
- 🗄️ MongoDB Storage (persistent & scalable)
- ⚡ Anti-Spam Delay System
- ☁️ Koyeb Deployment Ready

---

## 🧠 How It Works

1. Bot reads content from a **source channel**
2. Stores message IDs in database
3. Posts content to destination channel:
   - Based on daily limit
   - Spread across configured time window
4. Maintains sequence (loop system)
5. When new posts are added:
   - Automatically indexed
   - Appended to queue (no disruption)

---

## 🛠️ Commands

### 👤 Admin

/addadmin <user_id>

### 📡 Channel Setup

/addchannel <destination_id> <source_id> /removechannel <destination_id>

### ⚙️ Settings

/setlimit <channel_id> <number> /settime <channel_id> <start_hour> <end_hour> /setfooter <channel_id> <text> /setmode <channel_id> remove|replace|keep /setlink <channel_id> <link>

### 🎛️ Control

/pause <channel_id> /resume <channel_id>

### 📊 Info

/status /help

---

## ⚙️ Environment Variables

API_ID= API_HASH= SESSION_STRING= MONGO_URI= OWNER_ID=

---

## 🚀 Deployment (Koyeb)

1. Connect GitHub repo to Koyeb  
2. Add environment variables  
3. Set start command:

python -m bot.main

---

## ⚠️ Requirements

- Bot must be **admin in destination channels**
- Account must have access to **source channels**
- Use correct channel IDs (`-100xxxx`)

---

## 🧩 Tech Stack

- Python (Async)
- Telethon (Userbot API)
- MongoDB (Database)
- Koyeb (Hosting)

---

## 🔥 Use Cases

- Content reposting channels  
- Meme / reels automation  
- Niche content pipelines  
- Passive Telegram growth systems  

---

## 📌 Notes

- Bot does NOT reset sequence  
- New content is appended automatically  
- Each channel runs independently  

---

## 👑 Author

Made by [Maulik Patel](https://github.com/Maulikpatell)

---

## ⭐ Support

If you like this project, consider giving it a star ⭐


---

