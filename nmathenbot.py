from telegram import *
from telegram.ext import *
import logging
from pytube import YouTube, Playlist
import os
from moviepy.editor import *
from pydub import *
from dotenv import load_dotenv

def start_command(update, context):
    update.message.reply_text("Hello! Welcome to my new bot!\nThis bot can download youtube videos(less than 7 minutes).\nSend the link of the video or a playlist you want to download, the bot bot will download it for you.\nCheck /help for more details")

def help_command(update, context):
    update.message.reply_text("""
This bot will download youtube videos or playlists as mp4 or mp3 files according to your choice. 
Provide the bot with a valid link of a video or a playlist you want to download.

Limitations: 
* The bot can send files which are only less than 30MB of size. So kindly refrain from sending videos which are more than 8 minutes.
* The videos will be downlaoded in 360p as of now. 
 """)

def handle_message(update, context):
    global inputtext
    inputtext = str(update.message.text)

    if "www.youtube.com/watch?v=" in inputtext or "https://youtu.be/" in inputtext or "https://youtube.com/shorts" in inputtext:
        inlineButton =  [[InlineKeyboardButton("Video",callback_data="singleVideo"),
                          InlineKeyboardButton("Audio",callback_data="singleAudio")]
                        ]
        reply_markup = InlineKeyboardMarkup(inlineButton)

        update.message.reply_text("Download the youtube link as",reply_markup=reply_markup)
      
    elif "youtube.com/playlist?list=PL" in inputtext:
        inlineButton = [[InlineKeyboardButton("Video",callback_data="playlistVideo"),
                         InlineKeyboardButton("Audio",callback_data="playlistAudio")]
                       ]
        reply_markup = InlineKeyboardMarkup(inlineButton)

        update.message.reply_text("Download your playlist as",reply_markup=reply_markup)

    else:
        update.message.reply_text("Please provide a valid youtube link of videos or playlists!")

def toSingleVideo(update, context):
    #Sending as Video(mp4)
    yt = YouTube(inputtext)
    reply = update.callback_query.message #shortening update.callback_query.message to reply
    reply.reply_text("Downloading Video.....")
    video = yt.streams.get_by_resolution("360p").download()
    reply.reply_video(open(video,'rb'), caption=f"Title: {yt.title}\nQuality: 360p")
    os.remove(video)
    reply.reply_text("Video download Successfull")


def toSingleAudio(update, context):
    #Sending as Audio(mp3)
    yt = YouTube(inputtext)
    message = update.callback_query.message
    message.reply_text("Downloading Audio.....")
    AudioOnly = yt.streams.filter(only_audio=True).first().download()
    fullFileName = os.path.basename(AudioOnly)
    splitName = os.path.splitext(fullFileName)
    AudioFile = AudioFileClip(fullFileName)
    mp3FileName = splitName[0] + ".mp3"
    AudioFile.write_audiofile(mp3FileName)
    AudioFile.close()
    message.reply_audio(open(fullFileName,'rb'))#, caption=f"Title: {yt.title}\nDuration: {yt.length} seconds")
    os.remove(AudioOnly)
    os.remove(mp3FileName)
    message.reply_text("Audio download Successfull")


def toplaylistVideo(update, context):
    pl = Playlist(inputtext)
    message = update.callback_query.message
    message.reply_text("Downloading playlist as videos.....")
    for vid in pl.videos:
        video = vid.streams.get_by_resolution("360p").download()
        fullName = os.path.basename(video)
        splitName = os.path.splitext(fullName)
        newName = splitName[0] + ".mp4"
        os.rename(fullName,newName)
        message.reply_video(open(os.path.abspath(newName),'rb'), caption = f"Title: {vid.title}")
        os.remove(video)
    message.reply_text("Playlist video downloads successfull")


def toPlaylistAudio(update, context):
    pl = Playlist(inputtext)
    message = update.callback_query.message
    message.reply_text("Downloading playlist as audios.....")
    for vid in pl.videos:
        video = vid.streams.filter(only_audio=True).first().download()
        fullName = os.path.basename(video)
        splitName = os.path.splitext(fullName)
        newName = splitName[0] + ".mp4"
        os.rename(fullName,newName)
        audio = AudioFileClip(newName)
        audiomp3Name = splitName[0] + ".mp3"
        audio.write_audiofile(audiomp3Name)
        audio.close()
        message.reply_audio(open(fullName,'rb'))
        os.remove(video)
        os.remove(audiomp3Name)
    message.reply_text("Playlist audio downloads successfull")


def button(update, context):
    query = update.callback_query
    query.answer()
    if(query.data == "singleVideo"):
        toSingleVideo(update, context)
    if(query.data == "singleAudio"): 
        toSingleAudio(update, context)
    if(query.data == "playlistVideo"):
        toplaylistVideo(update, context)
    if(query.data == "playlistAudio"):
        toPlaylistAudio(update, context)


def error(update, context):
    logging.error(f"Update {update} caused error {context.error}")



if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    #Commands
    dp.add_handler(CommandHandler('start',start_command))
    dp.add_handler(CommandHandler('help',help_command))

    #Messages Test
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    #Button Handler
    dp.add_handler(CallbackQueryHandler(button))

    #Error handling
    dp.add_error_handler(error)

    updater.start_polling(3)
    updater.idle()


print("EXIT")
