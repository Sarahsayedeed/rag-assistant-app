import requests
import json
import time

questions = [
    "What command creates a Python virtual environment?",
    "ما الفرق بين WHERE و HAVING؟",
    "ما الفرق بين git fetch و git pull؟",
    "What are the ACID properties?",
    "Who won the 2018 FIFA World Cup?"
]

results = []
for q in questions:
    print(f"Testing: {q}")
    start_time = time.time()
    try:
        r = requests.post('http://localhost:8000/query', json={'question': q}, timeout=300)
        answer = r.json().get("answer", "")
        sources = r.json().get("sources", [])
        print(f"Time taken: {time.time() - start_time:.2f}s")
        print(f"Answer: {answer[:100]}...\n")
    except Exception as e:
        answer = str(e)
        sources = []
        print(f"Error: {e}\n")
        
    results.append({
        "question": q,
        "answer": answer,
        "sources": sources
    })

with open('all_tests.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
