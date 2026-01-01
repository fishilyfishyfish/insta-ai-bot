from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "insta_ai_verify"  # Meta에 입력할 토큰과 반드시 동일

@app.route("/")
def home():
    return "Server is running"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 🔹 Meta Webhook 검증용 (처음 저장할 때)
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    # 🔹 인스타 DM 이벤트 수신
    if request.method == "POST":
        print("INSTAGRAM EVENT:", request.json)
        return "EVENT_RECEIVED", 200
