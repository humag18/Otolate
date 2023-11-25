from flask import Flask, render_template, redirect, request, url_for
from main import getUsersSortedByScore, getLastChallenge

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('username.html')

@app.route('/createUsername', methods = ['POST'])
def login():
    # current username of the connected user
    username = request.form['username']
    return redirect(url_for('page', username=username))
@app.route('/page')
def page():
    currentUser = request.args.get('username', default=None)
    users = getUsersSortedByScore()
    challenge = getLastChallenge()[0]
    tool = getLastChallenge()[1]

    return render_template('page.html', users=users, username=currentUser, tool=tool, challenge=challenge)

@app.route('/challenges')
def challenges():
    currentUser = request.args.get('username', default=None)
    return render_template('challenges.html', users = [("Michel",12),("Pat",9),("Flav",14)], challenge = "Make a magic trick! AVADA KEDAVRA", challenges = ["mdr", "lol", "etc"], tool = "text", username = currentUser)

if __name__ == '__main__':
    app.run(debug=True)
