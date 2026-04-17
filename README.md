# Grok Log Extraction Tool

This is a Python script that extracts only the conversation parts from log data downloaded from Grok and converts them into a readable HTML format.

HTML files are generated for each chat in the format of "Conversation Title.html". In addition to HTML, the output is also provided in txt and json formats.

---

## Preparation

### Downloading Grok Logs

- Download and unzip your Grok log data from https://accounts.x.ai/data.

Caution
"prod-grok-backend.json" contains personal information such as chat history and timestamps.
Never commit this file to a repository. It is strongly recommended to add it to .gitignore.

---

### Installing Python

- Install Python 3.8 or higher from https://www.python.org/.
- This script does not require external libraries and runs using only the standard library.

---

### Placing the Script

- Place grok_log_export.py in the same folder as prod-grok-backend.json.

Caution
- When saving, set the "Save as type" to "All files".
- Make sure the extension is set to .py.

---

## How to Run

### Execute by Double-Clicking

- You can run the script by double-clicking the Python file.

---

### Execute via Terminal (Command Line)

#### Checking the Path

Example (Windows):

```
C:\Users\Username\Downloads...\export_data\alphanumeric_string\
```

---

#### Opening the Terminal

- Windows: Enter "cmd" in the search bar and press Enter.
- macOS/Linux: Open the Terminal.

---

#### Executing the Command

Windows:

```
cd "C:\Users\Username\Downloads\unzipped_log_folder\ttl\30d\export_data\alphanumeric_string\"
python grok_log_export.py
```

macOS/Linux:

```
cd /Users/Username/Downloads/unzipped_log_folder/ttl/30d/export_data/alphanumeric_string/
python3 grok_log_export.py
```

Caution
Depending on your environment, use "python3" instead of "python".

---

## Output Details

A folder is created for each conversation title, and the output is structured as follows:

```
/[Conversation_Title]/
  ├── html/
  │    ├── Conversation_Title.html   # Full duration log
  │    ├── YYYY-MM.html              # Monthly logs
  │    └── index.html                # Links to monthly and full logs
  ├── json/
  │    ├── Conversation_Title.json
  │    └── YYYY-MM.json
  └── txt/
       ├── Conversation_Title.txt
       └── YYYY-MM.txt
```

---

## Notes

- Only human/assistant one-on-one conversation pairs are extracted.
- Timestamps are displayed in Japan Standard Time (JST).
(Due to Grok's specifications, strict time zones are not guaranteed.)

---

## Unsupported Features

- Attachments within chats (images, files)
- Branched logs caused by regeneration
- Backend search results
- Agent features (e.g., generation by multiple personas)
- Logs from image and video generation

---

## Additional Information

- When run by double-clicking, the window may close automatically after the process is complete.

---

## Disclaimer

Use this script at your own risk.
The creator is not responsible for any damages caused by the use of this script.
