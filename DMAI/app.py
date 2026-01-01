from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "insta_ai_verify"

@app.route("/")
def home():
    return "Server is running"

@app.route("/privacy")
def privacy():
    return """
    <h1>Privacy Policy</h1>
    <p>This app is used for internal testing of Instagram messaging automation.</p>
    <p>No data is stored or shared.</p>
    <p>Contact: leunggi2@naver.com</p>
    """

@app.route("/terms")
def terms():
    return """
    <h1>Terms of Service</h1>
    <p>This service is provided for testing purposes only.</p>
    """

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    if request.method == "POST":
        print("INSTAGRAM EVENT:", request.json)
        return "EVENT_RECEIVED", 200
