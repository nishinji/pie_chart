import requests
from collections import Counter
import math
import svgwrite
import os

URL = "https://vita3k-api.pedro.moe/list/commercial"
OUTPUT_PATH = "images/chart.svg"

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

# 円グラフ用パラメータ
total = sum(sizes)
center = (200, 180)  # 円グラフの中心 (上に少し寄せる)
radius = 120
start_angle = -90  # 上方向からスタート

dwg = svgwrite.Drawing(OUTPUT_PATH, size=("400px", "400px"))
dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))  # 背景黒

# 円グラフ描画
for label, size, color in zip(labels, sizes, colors):
    angle = 360 * size / total
    end_angle = start_angle + angle

    # 扇形の終点
    x1 = center[0] + radius * math.cos(math.radians(start_angle))
    y1 = center[1] + radius * math.sin(math.radians(start_angle))
    x2 = center[0] + radius * math.cos(math.radians(end_angle))
    y2 = center[1] + radius * math.sin(math.radians(end_angle))

    # 大きな角度かどうか
    large_arc = 1 if angle > 180 else 0

    path = [
        f"M {center[0]},{center[1]}",
        f"L {x1},{y1}",
        f"A {radius},{radius} 0 {large_arc},1 {x2},{y2}",
        "Z"
    ]
    dwg.add(dwg.path(d=" ".join(path), fill=color, stroke="black", stroke_width=1))

    start_angle = end_angle

# 凡例を下に描画
legend_x = 40
legend_y = 340
legend_spacing = 20

for i, (label, size, color) in enumerate(zip(labels, sizes, colors)):
    y = legend_y + i * legend_spacing
    # 色ボックス
    dwg.add(dwg.rect(insert=(legend_x, y - 10), size=(15, 15), fill=color))
    # テキスト
    dwg.add(dwg.text(
        f"{label} ({size})",
        insert=(legend_x + 25, y + 2),
        fill="white",
        font_size="12px",
        alignment_baseline="middle"
    ))

# 保存
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
dwg.save()
