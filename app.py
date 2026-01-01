import os
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

# =========================
# 설정값
# =========================
VERIFY_TOKEN = "insta_ai_verify"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# 기본 확인용
# =========================
@app.route("/")
def home():
    return "Server is running"

# =========================
# Webhook
# =========================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1️⃣ Meta Webhook 검증
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    # 2️⃣ DM 이벤트 수신
    if request.method == "POST":
        data = request.json
        print("RAW EVENT:", data)

        # 메시지 텍스트 추출
        try:
            message_text = (
                data["entry"][0]
                    ["messaging"][0]
                    ["message"]
                    ["text"]
            )
        except Exception:
            return "EVENT_RECEIVED", 200

        # 3️⃣ @ai 호출 필터
        if "@ai" not in message_text.lower():
            return "EVENT_RECEIVED", 200

        # 4️⃣ 질문 정리 (@ai 제거)
        user_question = message_text.lower().replace("@ai", "").strip()
        print("QUESTION:", user_question)

        # 5️⃣ OpenAI 호출
        ai_reply = ask_ai(user_question)
        print("AI ANSWER:", ai_reply)

        # ❗ 여기서는 아직 DM으로 안 보냄
        # 다음 단계에서 send_message() 추가

        return "EVENT_RECEIVED", 200


# =========================
# OpenAI 함수
# =========================
def ask_ai(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 인스타그램 단체 DM방에 있는 AI야. "
                        "말투는 자연스럽고 짧게. "
                        "불렸을 때만 대답해."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OPENAI ERROR:", e)
        return "잠깐 오류가 났어. 다시 불러줘."
