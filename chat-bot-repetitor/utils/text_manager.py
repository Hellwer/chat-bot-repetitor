import json
import os
import time

DATA_FILE = 'data/texts.json'

def load_texts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_texts(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_texts(user_id):
    data = load_texts()
    return data.get(str(user_id), [])

def add_user_text(user_id, text):
    data = load_texts()
    user_texts = data.get(str(user_id), [])
    user_texts.append({
        'text': text,
        'learned_lines': 0,
        'total_lines': len(text.split('\n')),
        'time_started': time.time()  # Время начала изучения
    })
    data[str(user_id)] = user_texts
    save_texts(data)
