import json
from datetime import datetime

# JSONファイルの読み込み
with open('prod-grok-backend.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 各会話から情報を抽出
for convo in data['conversations']:
    title = convo['conversation'].get('title', 'Untitled')
    create_time = convo['conversation'].get('create_time', '1970-01-01T00:00:00Z')
    
    # 開始日をフォーマット（エラー対策）
    try:
        start_date = datetime.strptime(create_time, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        start_date = '不明な日付'
    
    # 対話ログを格納するリスト（タイムスタンプ付き）
    dialogues = []
    responses = convo['responses']
    i = 0
    while i < len(responses):
        resp = responses[i].get('response', {})
        sender = resp.get('sender', 'unknown')
        msg = resp.get('message', '').strip()
        timestamp = resp.get('create_time', {}).get('$date', {}).get('$numberLong', 0)
        time_str = datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S') if timestamp else '不明な時間'
        
        if sender == 'human':
            human_msg = msg
            human_time = time_str
            assistant_msg = ''
            assistant_time = '不明な時間'
            # 次のレスポンスがassistantならペアリング
            if i + 1 < len(responses) and responses[i + 1].get('response', {}).get('sender') == 'assistant':
                next_resp = responses[i + 1].get('response', {})
                assistant_msg = next_resp.get('message', '').strip()
                assistant_timestamp = next_resp.get('create_time', {}).get('$date', {}).get('$numberLong', 0)
                assistant_time = datetime.fromtimestamp(int(assistant_timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S') if assistant_timestamp else '不明な時間'
                i += 2
            else:
                # humanの連投の場合、次のhumanを独立したダイアログとして処理（ループ継続）
                i += 1
        elif sender == 'assistant':
            # assistantが先に来るか、連投の場合: humanを空にしてassistantだけ扱う
            human_msg = ''
            human_time = '不明な時間'
            assistant_msg = msg
            assistant_time = time_str
            i += 1
        else:
            # 不明なsenderはスキップ
            i += 1
            continue
        
        if human_msg or assistant_msg:
            dialogues.append({
                'human': {'message': human_msg, 'time': human_time},
                'assistant': {'message': assistant_msg, 'time': assistant_time}
            })
    
    # テキスト形式で整形
    formatted_text = f'「{title}」\n\n'
    formatted_text += f'チャット開始日: {start_date}\n\n'
    formatted_text += '会話ログ:\n\n'
    for dialogue in dialogues:
        if dialogue['human']['message']:
            formatted_text += f'「{dialogue["human"]["message"]}」\n'
            formatted_text += f'({dialogue["human"]["time"]})\n\n'
        if dialogue['assistant']['message']:
            formatted_text += f'「{dialogue["assistant"]["message"]}」\n'
            formatted_text += f'({dialogue["assistant"]["time"]})\n\n'

    # テキストファイルを保存
    with open(f'{title.replace(" ", "_")}.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(formatted_text)

    # JSONデータを保存
    json_data = {
        'チャット開始日': start_date,
        '会話ログ': dialogues
    }
    with open(f'{title.replace(" ", "_")}.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

    # HTML形式でチャットログを生成
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            background-color: #e0e0e0;
            padding: 20px;
        }}
        .chat-container {{
            padding: 0;
        }}
        .message {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            max-width: 60%;
            display: block;
            color: #000000;
            clear: both;
        }}
        .human {{
            background-color: #c0c0c0;
            float: right;
            text-align: left;
        }}
        .assistant {{
            background-color: #d0d0d0;
            float: left;
            text-align: left;
        }}
        .time {{
            font-size: 0.8em;
            color: #808080;
            display: block;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>{title}</h2>
        <p>チャット開始日: {start_date}</p>
        <div class="chat-log">
"""
    for dialogue in dialogues:
        if dialogue['human']['message']:
            html_content += f'            <div class="message human"><div>{dialogue["human"]["message"]}</div><div class="time">({dialogue["human"]["time"]})</div></div>\n'
        if dialogue['assistant']['message']:
            html_content += f'            <div class="message assistant"><div>{dialogue["assistant"]["message"]}</div><div class="time">({dialogue["assistant"]["time"]})</div></div>\n'
    html_content += """        </div>
    </div>
</body>
</html>"""

    # HTMLファイルを保存
    with open(f'{title.replace(" ", "_")}.html', 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

print("各チャットがタイトルごとに '.txt', '.json', と '.html' ファイルとして抽出されました。")