from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>LAB EX24</title>
        </head>
        <body>
            <h1>CI/CD Pipeline Using GitHub Actions</h1>
            <h2>Flask Application</h2>
            <p>Application is running successfully!</p>
            <p>Docker + GitHub Actions</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "message": "Flask application is running"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)