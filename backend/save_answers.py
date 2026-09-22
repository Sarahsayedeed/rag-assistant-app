import requests
import json
import time

questions = [
    "ما الفرق بين WHERE و HAVING؟",
    "ما الفرق بين git fetch و git pull؟",
    "What are the ACID properties?",
    "Who won the 2018 FIFA World Cup?"
]

results = {}
for q in questions:
    try:
        r = requests.post('http://localhost:8000/query', json={'question': q}, timeout=300)
        results[q] = r.json().get('answer', '')
    except Exception as e:
        results[q] = f"Error: {e}"

with open('final_answers.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
