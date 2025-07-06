# 📬 MailTagger 
Your inbox, auto-organized. Label Gmail messages by sender or keyword — effortlessly.

Automatically organize your Gmail inbox by labeling emails based on sender names or keywords in the subject and body.  
This script uses the Gmail API and a customizable config file (`label_rules.json`) to apply labels, archive noise, and declutter your inbox.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Gmail API](https://img.shields.io/badge/Gmail%20API-Enabled-green)
![Status](https://img.shields.io/badge/auto--labeler-active-brightgreen)

---

## ✨ Features

- 🔖 Automatically applies Gmail labels based on custom rules
- 📂 Detects emails by **sender name** or **keywords in subject/body**
- 🏷️ Creates labels if they don’t already exist
- 📤 Optionally archives emails from specific categories
- 🛡️ Sensitive files like credentials are `.gitignore`d
- 🔧 Fully configurable through `label_rules.json`

---

## 📁 Project Structure

- gmail_autolabel.py # Main script
- label_rules.example.json # Template for user-defined labeling rules
- .gitignore # Excludes secrets from version control
- requirements.txt # Python dependencies

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash

git clone https://github.com/joselynrianaaa/MailTagger.git

cd gmail-autolabel

```
### 2. Install Dependencies

```bash

pip install -r requirements.txt
```
### 3. Set Up Gmail API Access

- Go to Google Cloud Console

- Create a new project

- Enable the Gmail API

- Go to APIs & Services > Credentials

- Create OAuth 2.0 Credentials (Application type: Desktop App)

- Download the credentials.json file and place it in the project folder

✅ When you run the script for the first time, it will open a browser window to authenticate.

A token.json will be created automatically and reused in future runs.

✏️ Customizing Rules

Copy the example file and rename it:

```bash


cp label\_rules.example.json label\_rules.json
```
Then open label\_rules.json and define your labels:

```bash
{

"Work": {

"senders": \["manager@company.com", "hr@company.com"\],

"keywords": \["project update", "meeting agenda"\]

},

"Courses": {

"senders": \["noreply@onlinecourses.com"\],

"keywords": \["new course", "certificate"\]

},

"Spam": {

"keywords": \["lottery", "win big", "free money"\]

}

}
```
"senders" match the From field (partial or full, case-insensitive)

"keywords" match words in the subject or body

You can skip "senders" or "keywords" if only one is needed

## 🚀 Running the Script

```bash



python gmail\_autolabel.py
```
You'll see console output showing which labels were applied and whether any emails were archived.

## 🛑 Important Notes

This script modifies your Gmail inbox — test it carefully on a few emails first

Any label not found will be automatically created

Archiving behavior can be configured in the script logic

## 🔐 .gitignore

Your .gitignore should include:

- pgsql

- credentials.json

- token.json

- label\_rules.json

- \_\_pycache\_\_/

- \*.pyc

This keeps sensitive info out of version control.

## 🧠 Ideas for Future Improvement

- Add CLI flags (e.g., --unread-only, --dry-run)

- Export logs to CSV or JSON

- Streamlit web interface for rule editing

- Schedule script to run daily with Task Scheduler

## 👩‍💻 Author

**Joselyn Riana**  

