from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "EX20 - GitHub Version Control"

@app.route("/team")
def team():
    return "Team Project - Version Control Demonstration"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)