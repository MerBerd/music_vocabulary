from flask import Flask, render_template, request
from string import ascii_uppercase
import psycopg2
import os

app = Flask(__name__)

#conn = psycopg2.connect("dbname=music_voc user=postgres password=mergen")
conn = psycopg2.connect(dbname="d4pem9453rm7l3",
user=os.environ.get("DB_USER"),
password=os.environ.get("DB_PASSWORD"),
host=os.environ.get("DB_HOST"),
port="5432")
cur = conn.cursor()

app.config['JSON_AS_ASCII'] = False


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("SignUp.html")
    else:
        pass  # for post method


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("LogIn.html")
    else:
        pass  # for post method


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        word = str(request.form.get("word")).upper()
        cur.execute("SELECT word, translation, definition FROM vocabulary WHERE word LIKE  %s", ("%" + word +
                                                                                                 "%",))
        word_data = cur.fetchall()
        if not word_data:
            return render_template("error.html")
        return render_template("word.html", data=word_data)
    else:
        return render_template("index.html")


@app.route('/vocabulary')
def vocabulary():
    cur.execute("SELECT * FROM vocabulary")
    vocab = cur.fetchall()
    voc = {}
    for letter in ascii_uppercase:
        voc[letter] = []

    for word in vocab:
        if word[1][0]:
            voc[word[1][0]].append(word)
        else:
            pass

    for word in list(voc):
        if not voc[word]:
            voc.pop(word)

    return render_template("vocabulary.html", vocabulary=voc)


@app.route('/liked', methods=["GET", "POST"])
def liked():
    if request.method == "POST":
        liked_word = request.form.get("word")
        return liked_word
    else:
        pass

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
