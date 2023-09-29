import os
import speech_recognition as sr
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatActions
from moviepy.editor import AudioFileClip

BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

output_directory = 'audio_output'
os.makedirs(output_directory, exist_ok=True)
recognizer = sr.Recognizer()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Welcome to the Speech to Text bot! Send me a voice message, and I will convert it to text.")


@dp.message_handler(content_types=types.ContentType.VOICE)
async def convert_audio(message: types.Message):
    await message.answer_chat_action(ChatActions.TYPING)

    voice_file = await message.voice.get_file()
    voice_path = os.path.join(output_directory, voice_file.file_id + '.ogg')
    await voice_file.download(voice_path)

    wav_path = os.path.join(output_directory, voice_file.file_id + '.wav')
    audio_clip = AudioFileClip(voice_path)
    audio_clip.write_audiofile(wav_path)

    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='fa-IR')
        except sr.UnknownValueError:
            text = "Sorry, I couldn't understand the audio."
        except sr.RequestError as e:
            text = f"Sorry, there was an error with the speech recognition service: {str(e)}"

    await message.reply(text)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
