from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"

if __name__ == "__main__":
    app.run()