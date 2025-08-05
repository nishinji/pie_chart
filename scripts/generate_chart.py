import requests
import matplotlib.pyplot as plt
from collections import Counter
import os

URL = "https://vita3k-api.pedro.moe/list/commercial"
OUTPUT_PATH = "images/chart.png"

status_order = [
    "Nothing", "Bootable", "Intro", "Menu", "Ingame -", "Ingame +", "Playable"
]

# データ取得
response = requests.get(URL)
data = response.json()
games = data.get("list", [])

status_counter = Counter()
status_color_map = {}

for entry in games:
    status = entry.get("status", "Unknown")
    color = entry.get("color", "999999")
    status_counter[status] += 1
    if status not in status_color_map:
        status_color_map[status] = f"#{color}"

labels = [s for s in status_order if s in status_counter]
sizes = [status_counter[s] for s in labels]
colors = [status_color_map[s] for s in labels]

# グラフ描画設定（背景黒、ラベル白）
fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,  # ← 上方向から開始
    colors=colors,
    textprops={'color': 'white'}
)

plt.axis('equal')

# 保存
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, bbox_inches="tight", facecolor=fig.get_facecolor(), transparent=True)
