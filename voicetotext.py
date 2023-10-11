import os

os.system("pip install telebot ; pip install speech_recognition")

import telebot
import speech_recognition as sr

# Создаем экземпляр бота
bot = telebot.TeleBot('6318973044:AAHVsPivDWCe07Zm03qIiN5pfGRnMw153dk')

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    # Получаем информацию о первом голосовом сообщении из списка голосовых сообщений
    voice_info = message.voice
    file_id = voice_info.file_id

    # Загружаем аудиофайл с помощью метода getFile
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Создаем временный файл для сохранения аудиофайла
    audio_filename = 'audio.ogg'
    with open(audio_filename, 'wb') as f:
        f.write(downloaded_file)
    
    # Создаем объект для распознавания речи
    recognizer = sr.Recognizer()
    
    try:
        # Открываем временный аудиофайл и переводим аудио в текст
        with sr.AudioFile(audio_filename) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="ru-RU")
        bot.send_message(message.chat.id, "Вы сказали: " + text)
        
    except sr.UnknownValueError:
        bot.send_message(message.chat.id, "Не удалось распознать речь")
    except sr.RequestError as e:
        bot.send_message(message.chat.id, f"Ошибка сервиса распознавания речи: {e}")
    
    # Удаляем временный аудиофайл
    os.remove(audio_filename)

# Запускаем бота
bot.polling()
