import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
import requests

token_ai = "token_ai.txt"
with open(token_ai, 'r') as file:
    token_ai = file.read().strip()

token_j = "token_3.txt"
with open(token_j, 'r') as file:
    bot_token = file.read().strip()


client = OpenAI(
   api_key= token_ai #os.environ.get("OPENAI_API_KEY"),
)

def draw_ai(text):
  response = client.images.generate(
            model="dall-e-3",
            prompt=text,
            size="1024x1024",
            quality="standard",
            n=1,
  )
  i = 0
  for item in response.data:
      i = i + 1
      image_url = item.url
      # Download the image
      image_response = requests.get(image_url)
      image_data = image_response.content
      # Save the image to a file
      with open(f"generated_image_{i}.jpg", "wb") as image_file:
          image_file.write(image_data)
      print(f"Image saved to 'generated_image_{i}.jpg'")


# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')

@bot.message_handler(content_types=['photo'])
def process_image(message):
    bot.reply_to(message.chat.id, "Прости, я не работаю с фото")

@bot.message_handler(content_types=['voice'])
def process_voice_message(message):
    # Получаем информацию о голосовом сообщении
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    # Скачиваем голосовое сообщение
    downloaded_file = bot.download_file(file_path)
    # Сохраняем голосовое сообщение на диск
    voice_file_path = 'voice_message.ogg'
    with open(voice_file_path, 'wb') as f:
        f.write(downloaded_file)
    # Преобразование голосового сообщения в текст
    input_file = 'voice_message.ogg'
    audio = AudioSegment.from_file(input_file, format='ogg')
    # Конвертация в формат WAV
    output_file = 'audio.wav'
    audio.export(output_file, format='wav')
    recognizer = sr.Recognizer()
    with sr.AudioFile(output_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='ru')  # Здесь можно указать другой язык, если нужно
    command = text.split(' ')[0]
    bot.reply_to(message, text)
    if (command == 'нарисуй'):
      draw_ai(text)
      with open('generated_image_1.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)
    # Удаляем временные файлы
    os.remove(output_file)

bot.polling()