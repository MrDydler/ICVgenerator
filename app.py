from icalendar import Calendar, Event
from datetime import datetime
from flask import Flask, request, jsonify
import os
import time
from telegram import Bot

app = Flask(__name__)

def generate_ics(summary, start, end, description):
    start_datetime = datetime.strptime(start, '%Y-%m-%d %H:%M')
    end_datetime = datetime.strptime(end, '%Y-%m-%d %H:%M')

    # Создание календаря
    cal = Calendar()

    # Создание ивента
    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    # Добавление ивента в календарь
    cal.add_component(event)

    # Генерация ics контента
    return cal.to_ical()

@app.route('/generate_ics', methods=['POST'])
async def handle_generate_ics():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    summary = data.get('summary')
    start = data.get('start')
    end = data.get('end')
    description = data.get('description')
    chat_id = data.get('chat_id')

    if not all([summary, start, end, description]):
        return jsonify({'error': 'Missing required fields'}), 400

    ics_content = generate_ics(summary, start, end, description)

    # Отправка в телегу
    bot_token = '6456266993:AAFpP4deSDVyMps7uO22n3CQLC5ZzHPeaeo'
    #chat_id = '938563450'
    bot = Bot(token=bot_token)
    bot.send_document(chat_id=chat_id, document=ics_content, filename=f'{summary}.ics')
    time.sleep(5)

    return jsonify({'message': 'Календарь создан и отправлен в Telegram'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
