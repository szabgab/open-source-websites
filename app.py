from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html', title="Open Source Web Sites")

if __name__ == "__main__":
    app.run(debug=True)
