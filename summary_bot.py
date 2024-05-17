import telebot
import os
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
import requests
import re

token_ai = "token_ai.txt"
with open(token_ai, 'r') as file:
    token_ai = file.read().strip()

token_j = "token_2.txt"
with open(token_j, 'r') as file:
    bot_token = file.read().strip()

client = OpenAI(
   api_key= token_ai #os.environ.get("OPENAI_API_KEY"),
)

def split_text(text, max_chunk_size = 2048):    
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Функция для генерации краткого содержания текста с использованием OpenAI GPT-3
def generate_summary(text, max_chunk_size=2048):
    input_chunks = split_text(text, max_chunk_size)    
    output_chunks = []    
    # Задание промпта для модели
    prompt = " выдели только самые важные тезисы очень кратко "
    # Итерация по каждому куску входного текста
    for i, chunk in enumerate(input_chunks):
        # Запрос к модели GPT-3 для генерации тезисов на основе текущего куска текста
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt + chunk}
            ],
            temperature=0.1
        )        
        # Извлечение сгенерированного ответа от модели
        answer = response.choices[0].message.content     
        # Добавление сгенерированного куска в список
        output_chunks.append(answer)    
    # Объединение сгенерированных кусков в одну строку и возврат результата
    return " ".join(output_chunks)

# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')

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
    
    prompt = " из текста ниже выдели самое главное самое важное структурировано без придумывания своего " + text
    summary = " Если кратко, то: " + generate_summary(prompt)
    escaped_text = re.sub(r'([\"\\])', r'\\\1', summary)
    bot.reply_to(message, escaped_text)
    
    # Удаляем временные файлы
    os.remove(output_file)

bot.polling()