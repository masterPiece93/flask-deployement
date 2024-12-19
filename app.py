from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <h1 style="
        text-align: center;
        background: #000000;
        color: #FFD700;
        border: 0.1em solid gold;
        "
    >
    THE ANKIT </h1>

    <div style="text-align: center;">
    <a href="/ankit-loves-shalu">
    <i class="fa fa-heart" style="font-size:48px;color:red">
    </i>
    </a>
    </div>
    """

@app.route('/health')
def health():
    return {"healthy": True}

@app.route('/ankit-loves-shalu')
def message_1():
    return render_template('shalu.html')

