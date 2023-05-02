from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
RESPONSES_KEY = "responses"


@app.route('/')
def show_survey_start():
    """Choosing a survey"""
    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """"Clears the survey if responses"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

app.route("/answer", method=["POST"])
def handle_question():
    """This will redirect you to the next question but will save the response of the previous question"""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.question)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    responses = session.get(RESPONSES_KEY)
    if(responses is None):
        return redirect('/')
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    question = survey.questions[qid]
    return render_template("question.hmtl", question_num = qid, question=question)

@app.route("/complete")
def complete():
    return render_template("completion.html")