from flask import Flask, render_template ,request,flash,url_for,redirect
from pyexpat.errors import messages
import api
from db import Database

app =Flask(__name__)

dbo=Database()

@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/perform_registration', methods=['post'])
def perform_registration():
    u_name= request.form.get('name')
    u_email= request.form.get('email')
    u_password= request.form.get('password')

    response=dbo.insert(u_name, u_email, u_password)

    if response:
        return render_template("login.html", message='Registration Successful Kindly Login Now')

    else:
        return render_template('register.html', message="Email Already Exists, Please Try Again ")

@app.route("/perform_login", methods=['post'])
def perform_login():
    u_email= request.form.get('email')
    u_password= request.form.get('password')

    response= dbo.login(u_email,u_password)

    if response:
        return redirect('/profile')
    else:
        return render_template('login.html', message='Either mail/password is Incorrect')


@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/ner")
def ner():
    return render_template('ner.html')

@app.route('/perform_ner', methods=['POST'])
def perform_ner():
    u_txt = request.form.get('txt')
    response = api.ner(u_txt)

    entities = response.get('entities', [])
    return render_template('ner_result.html', entities=entities, text=u_txt)

@app.route('/sentiment')
def sentimnet():
    return render_template('sentiment.html')



@app.route('/perform_sentiment', methods=['POST'])
def perform_sentiment():
    u_txt = request.form.get('txt')
    result = api.sentiment(u_txt)

    polarity = round(result['polarity'], 2)
    subjectivity = round(result['subjectivity'], 2)

    # Assign emoji and message
    if polarity > 0.2:
        emoji = "😊"
        message = "This sounds positive and cheerful!"
    elif polarity < -0.2:
        emoji = "😞"
        message = "Hmm... that feels a bit negative."
    else:
        emoji = "😐"
        message = "Seems pretty neutral."

    return render_template(
        'sentiment_result.html',
        emoji=emoji,
        polarity=polarity,
        subjectivity=subjectivity,
        input_text=u_txt,
        message=message
    )


@app.route('/keyword')
def keyword_page():
    return render_template("keywords.html")

@app.route('/perform_keywords', methods=['POST'])
def perform_keywords():
    u_txt = request.form.get('txt')
    keywords = api.extract_keywords(u_txt)

    return render_template("keywords_result.html", input_text=u_txt, keywords=keywords)













app.run(debug=True)