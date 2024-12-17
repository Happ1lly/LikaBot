import os
import telebot
from pytube import YouTube
from moviepy.editor import AudioFileClip

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


# Command handler: Start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Good morning Lika, I'm here specially for u, My name is MiniVolo, and I was created for you to use me)\nSend me a YouTube link, and I'll convert it to an MP3!")


# Message handler: Process YouTube link
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        url = message.text
        if 'youtube.com' in url or 'youtu.be' in url:
            bot.reply_to(message, "Downloading the video... Please wait!")

            # Download YouTube video
            yt = YouTube(url)
            video_stream = yt.streams.filter(only_audio=True).first()
            downloaded_file = video_stream.download(filename='temp_video')

            # Convert video to MP3
            mp3_filename = 'output.mp3'
            clip = AudioFileClip(downloaded_file)
            clip.write_audiofile(mp3_filename)
            clip.close()
            os.remove(downloaded_file)  # Delete the temporary video

            # Send MP3 back to the user
            with open(mp3_filename, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(mp3_filename)  # Clean up

            bot.reply_to(message, "Here is your MP3 file! 🎧")
        else:
            bot.reply_to(message, "Please send a valid YouTube link.")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Something went wrong! Please try again.")


# Polling the bot
print("Bot is running...")
bot.polling()
