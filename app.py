from flask import Flask, render_template, request, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
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
    if question_id != len(responses) and question_id != 0:
        flash("Invalid question ID.")
        return redirect(url_for("show_question", question_id=len(responses)))
    if question_id >= len(satisfaction_survey.questions):
        return redirect(url_for("thank_you"))
    question = satisfaction_survey.questions[question_id]
    return render_template("question.html", question=question)


@app.route("/answer", methods=["POST"])
def handle_answer():
    answer = request.form["answer"]
    responses.append(answer)
    next_question_id = len(responses)
    if next_question_id >= len(satisfaction_survey.questions):
        return redirect(url_for("thank_you"))
    else:
        return redirect(url_for("show_question", question_id=next_question_id))


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")
