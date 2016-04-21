from flask import Flask, render_template
import datetime

now = datetime.datetime.now()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html', year=now.year)


if __name__ == '__main__':
    app.run(debug=True)
