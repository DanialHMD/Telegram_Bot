from flask import Flask, request
import requests
import os
#test
app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    return response.ok

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    data = request.json

    # GitHub Actions Workflow Failure
    if data.get("action") == "completed" and data.get("workflow_run"):
        run = data["workflow_run"]
        if run["conclusion"] == "failure":
            repo = run["repository"]["full_name"]
            workflow = run["name"]
            commit = run["head_commit"]["message"]
            url = run["html_url"]
            message = f"🚨 *Test Failure in GitHub Actions*\n*Repo:* {repo}\n*Workflow:* {workflow}\n*Commit:* `{commit}`\n🔗 [View Run]({url})"
            send_telegram_message(message)
    return "", 200

if __name__ == "__main__":
    app.run(port=5000)
