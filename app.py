from flask import Flask, render_template, request, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask import session
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def start():
    return render_template("start.html", survey=satisfaction_survey)


@app.route("/questions/<int:question_id>")
def show_question(question_id):
    if question_id != len(session["responses"]) and question_id != 0:
        flash("Invalid question ID.")
        return redirect(url_for("show_question", question_id=len(session["responses"])))

    question = satisfaction_survey.questions[question_id]
    return render_template("question.html", question=question, question_id=question_id)


@app.route("/answer", methods=["POST"])
def handle_answer():
    answer = request.form["answer"]

    session["responses"].append(answer)
    session.modified = True

    next_question_id = len(session["responses"])

    if next_question_id >= len(satisfaction_survey.questions):
        return redirect(url_for("thank_you"))
    else:
        return redirect(url_for("show_question", question_id=next_question_id))


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


@app.route("/start-survey", methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect(url_for("show_question", question_id=0))
