import requests
import time

time.sleep(2)

r = requests.get('https://thouvrun.onrender.com/api/scores', timeout=10)
scores = r.json()

print(f'📊 Scores actuels: {len(scores)}')
if len(scores) > 0:
    top = sorted(scores, key=lambda x: x.get('score_total', 0), reverse=True)[:5]
    print(f'\n🏆 Top 5:\n')
    for i, s in enumerate(top, 1):
        print(f'  {i}. {s["nom"]:<20} - {s["score_total"]:>3} pts')
