import json


def save_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f)

def save_text(filename, text: str):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)