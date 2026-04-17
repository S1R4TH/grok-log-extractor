import json
from datetime import datetime
import html
import os
import re
from collections import defaultdict

print("""
========================================
Grok Log Extraction Tool

- Extract chat logs by conversation title
- Split logs by month (txt / json / html)
- Generate HTML viewer with index
- Export full combined log files

* Extracts only human/assistant conversation pairs
* Attachments within chats are not supported
========================================
""")

# ===== Load JSON =====
with open('prod-grok-backend.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conversations = data.get('conversations', [])
total_convos = len(conversations)

# ===== List Available Titles =====
titles = sorted({
    c.get('conversation', {}).get('title', '')
    for c in conversations if c.get('conversation', {}).get('title')
})

print("\n=== Available Conversations ===")
for t in titles:
    print("-", t)
print("====================\n")

title_filter = input("Enter the chat title to extract (press Enter for all): ").strip()

# ===== CSS =====
CSS = """
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    background-color: #e0e0e0;
    padding: 20px;
}
.chat-container {
    padding: 0;
}
.message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
    max-width: 60%;
    display: block;
    clear: both;
}
.human {
    background-color: #c0c0c0;
    float: right;
}
.assistant {
    background-color: #d0d0d0;
    float: left;
}
.time {
    font-size: 0.8em;
    color: #808080;
    margin-top: 5px;
}
a, a:visited {
    color: #000;
    text-decoration: none;
}
.year-box {
    background-color: #d0d0d0;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
}
.month-list a {
    display: inline-block;
    margin: 5px 10px;
    font-weight: bold;
}
.full-log {
    display: block;
    margin-bottom: 20px;
    font-size: 1.2em;
    font-weight: bold;
}
"""

# ===== Main Process =====
for idx, convo in enumerate(conversations):

    percent = int((idx + 1) / total_convos * 100)
    print(f"\rProcessing... {percent}% ({idx+1}/{total_convos})", end="")

    title = convo.get('conversation', {}).get('title', 'Untitled')

    if title_filter and title.lower() != title_filter.lower():
        continue

    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)

    txt_dir = os.path.join(safe_title, "txt")
    json_dir = os.path.join(safe_title, "json")
    html_dir = os.path.join(safe_title, "html")

    os.makedirs(txt_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(html_dir, exist_ok=True)

    responses = convo.get('conversation', {}).get('responses', []) or convo.get('responses', [])

    monthly_logs = defaultdict(list)
    all_logs = []

    # ===== Extract Logs =====
    i = 0
    while i < len(responses) - 1:
        r1 = responses[i].get('response', {})
        r2 = responses[i + 1].get('response', {})

        if r1.get('sender') == 'human' and r2.get('sender') == 'assistant':
            msg_h = r1.get('message', '').strip()
            msg_a = r2.get('message', '').strip()

            ts_h = r1.get('create_time', {}).get('$date', {}).get('$numberLong', 0)
            ts_a = r2.get('create_time', {}).get('$date', {}).get('$numberLong', 0)

            if not ts_h:
                i += 1
                continue

            dt_h = datetime.fromtimestamp(int(ts_h) / 1000)
            dt_a = datetime.fromtimestamp(int(ts_a) / 1000) if ts_a else dt_h

            month = dt_h.strftime('%Y-%m')

            log = {
                "human": {
                    "message": msg_h,
                    "time": dt_h.strftime('%Y-%m-%d %H:%M:%S')
                },
                "assistant": {
                    "message": msg_a,
                    "time": dt_a.strftime('%Y-%m-%d %H:%M:%S')
                }
            }

            monthly_logs[month].append(log)
            all_logs.append(log)

            i += 2
        else:
            i += 1

    if not all_logs:
        continue

    months = sorted(monthly_logs.keys())

    # ===== Monthly Output (TXT / JSON / HTML) =====
    for month in months:
        logs = monthly_logs[month]

        # TXT
        with open(os.path.join(txt_dir, f"{month}.txt"), "w", encoding="utf-8") as f:
            for d in logs:
                f.write(f'「{d["human"]["message"]}」\n({d["human"]["time"]})\n')
                f.write(f'「{d["assistant"]["message"]}」\n({d["assistant"]["time"]})\n\n')

        # JSON
        with open(os.path.join(json_dir, f"{month}.json"), "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        # HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} - {month}</title>
<style>{CSS}</style>
</head>
<body>
<div class="chat-container">
<h1>{title}</h1>
<h2>{month}</h2>
"""

        for d in logs:
            html_content += f"""
<div class="message human">
{html.escape(d["human"]["message"])}
<div class="time">{d["human"]["time"]}</div>
</div>

<div class="message assistant">
{html.escape(d["assistant"]["message"])}
<div class="time">{d["assistant"]["time"]}</div>
</div>
"""

        html_content += "</div></body></html>"

        with open(os.path.join(html_dir, f"{month}.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    # ===== index =====
    year_map = defaultdict(list)
    for m in months:
        y, mo = m.split("-")
        year_map[y].append((int(mo), m))

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="chat-container">

<h1>{title}</h1>
<a class="full-log" href="{safe_title}.html">Full Log</a>

<h2>Monthly Log Index</h2>
"""

    for y in sorted(year_map.keys()):
        index_html += f'<div class="year-box"><h3>{y}</h3><div class="month-list">'
        for mo, full in sorted(year_map[y]):
            index_html += f'<a href="{full}.html">{mo}</a>'
        index_html += "</div></div>"

    index_html += "</div></body></html>"

    with open(os.path.join(html_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # ===== Full Log Export =====

    # TXT
    with open(os.path.join(txt_dir, f"{safe_title}.txt"), "w", encoding="utf-8") as f:
        for d in all_logs:
            f.write(f'「{d["human"]["message"]}」\n({d["human"]["time"]})\n')
            f.write(f'「{d["assistant"]["message"]}」\n({d["assistant"]["time"]})\n\n')

    # JSON
    with open(os.path.join(json_dir, f"{safe_title}.json"), "w", encoding="utf-8") as f:
        json.dump(all_logs, f, ensure_ascii=False, indent=2)

    # HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="chat-container">
<h1>{title}</h1>
<h2>Full Log</h2>
"""

    for d in all_logs:
        html_content += f"""
<div class="message human">
{html.escape(d["human"]["message"])}
<div class="time">{d["human"]["time"]}</div>
</div>

<div class="message assistant">
{html.escape(d["assistant"]["message"])}
<div class="time">{d["assistant"]["time"]}</div>
</div>
"""

    html_content += "</div></body></html>"

    with open(os.path.join(html_dir, f"{safe_title}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

print("\n\nAll tasks completed.")

# Prevent the window from closing immediately when run by double-click
import sys

if sys.stdin.isatty():
    input("\nPress Enter to exit...")
