from flask import Flask, request

app = Flask(__name__)

# Meta Webhook Verify Token (Meta 설정에 입력한 값과 반드시 동일)
VERIFY_TOKEN = "insta_ai_verify"

@app.route("/")
def home():
    return "Server is running"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # =========================
    # 1️⃣ Webhook 검증 (Meta가 처음 확인할 때)
    # =========================
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    # =========================
    # 2️⃣ DM 이벤트 수신
    # =========================
    if request.method == "POST":
        data = request.json
        print("RAW EVENT:", data)

        # 메시지 텍스트 추출 (구조가 다를 수 있어서 try-except)
        try:
            message_text = (
                data["entry"][0]
                    ["messaging"][0]
                    ["message"]
                    ["text"]
            )
        except Exception:
            # 텍스트 메시지가 아니면 무시
            return "EVENT_RECEIVED", 200

        # =========================
        # 3️⃣ 호출어 필터 (@ai 있을 때만 반응)
        # =========================
        triggers = ["@ai"]

        if not any(t in message_text.lower() for t in triggers):
            # @ai 없으면 조용히 무시
            return "EVENT_RECEIVED", 200

        # =========================
        # 4️⃣ 여기까지 오면 AI가 불린 것
        # =========================
        print("AI CALLED:", message_text)

        # ⚠️ 지금은 아직 '답장' 안 보냄
        # 다음 단계에서:
        # - OpenAI API 호출
        # - Instagram DM으로 답장 전송
        # 이 부분을 여기에 추가하면 됨

        return "EVENT_RECEIVED", 200
