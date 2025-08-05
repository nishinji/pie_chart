import requests
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import os

URL = "https://vita3k-api.pedro.moe/list/commercial"
OUTPUT_PATH = "images/chart.png"

# ステータスの表示順
status_order = [
    "Nothing",
    "Bootable",
    "Intro",
    "Menu",
    "Ingame -",
    "Ingame +",
    "Playable"
]

# API取得
response = requests.get(URL)
try:
    data = response.json()
    games = data.get("list", [])
    if not isinstance(games, list):
        raise ValueError("Expected a list under 'list' key.")
except Exception as e:
    print("❌ JSON parse error or unexpected format:", e)
    print("Raw content:", response.text[:500])
    exit(1)

# ステータスごとの件数と色（複数ゲームの中で最初に出てきた色を採用）
status_counter = Counter()
status_color_map = {}

for entry in games:
    if isinstance(entry, dict):
        status = entry.get("status", "Unknown")
        color = entry.get("color", "999999")  # fallback: gray
        status_counter[status] += 1
        if status not in status_color_map:
            status_color_map[status] = f"#{color}"  # prepend '#' for matplotlib

# グラフ用データ構築
labels = []
sizes = []
colors = []

for status in status_order:
    if status in status_counter:
        labels.append(status)
        sizes.append(status_counter[status])
        colors.append(status_color_map.get(status, "#999999"))  # fallback color

# 円グラフ描画
plt.figure(figsize=(6, 6))
plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors  # ← ここで色指定！
)
plt.axis('equal')

# 保存
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, bbox_inches="tight")
