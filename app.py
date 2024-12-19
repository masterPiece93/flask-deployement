from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1 style="
        text-align: center;
        background: #000000;
        color: #FFD700;
        border: 0.1em solid gold;
        "
    >
    THE ANKIT </h1>
    """

@app.route('/health')
def health():
    return {"healthy": True}
