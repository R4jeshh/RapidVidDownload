import yt_dlp
import re
import os
from pyrogram import Client, filters

# Bot Credentials
BOT_TOKEN = "8049510591:AAHL2DUiaZeGVX1hQPZoVaD1igpgeBkVsLE"
API_ID = "21003274"
API_HASH = "47bbfbda757efd499b84edffcbe2f269"

# Initialize Bot
app = Client("video_downloader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ----------------- Download Function -----------------
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info.get("title", "Unknown"), ydl.prepare_filename(info)

# ----------------- Start Command -----------------
@app.on_message(filters.command("start"))
async def start(_, message):
    welcome_message = """
    👋 **Welcome to Video Downloader Bot!**

    **How to Use:**
    - Just send me a YouTube or Adult website video link using `/dl {URL}` command.
    
    **Supported Websites:**
    ✅ **YouTube**
    ✅ **Pornhub**
    ✅ **Xvideos**
    ✅ **RedTube**
    ✅ **Other Adult Websites**
    
    I'll fetch the video for you and send it directly here in Telegram! 🚀
    
    💬 Send `/dl {URL}` to start downloading your videos.
    """
    await message.reply_text(welcome_message)

# ----------------- Download Command -----------------
@app.on_message(filters.command("dl") & filters.private)
async def downloader(_, message):
    # Get the URL after the /dl command
    url = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None

    if not url or not re.search(r"(youtube\.com|youtu\.be|pornhub\.com|xvideos\.com|redtube\.com)", url):
        await message.reply_text("❌ **Invalid URL!**\nPlease send a valid YouTube or Adult website video link.")
        return
    
    await message.reply_text("⏳ **Processing your request... Please wait!**")
    
    try:
        title, filepath = download_video(url)
        
        # Send Video
        await message.reply_video(
            video=filepath, 
            caption=f"🎥 **{title}**\n✅ Downloaded Successfully!"
        )
        
        # Delete File After Sending
        os.remove(filepath)
    except Exception as e:
        await message.reply_text(f"⚠️ **Error:** {str(e)}")

# Run the Bot
app.run()
