from flask import Flask, render_template, redirect, request, url_for
from main import getUsersSortedByScore, getLastChallenge, getUserByName, createUser

app = Flask(__name__)

current_user_glob = None

@app.route('/')
def home():
    return render_template('username.html')


@app.route('/createUsername', methods=['POST'])
def login():
    # current username of the connected user
    global current_user_glob
    current_user_glob = request.form['username']
    return redirect(url_for('page'))


@app.route('/page')
def page():
    global current_user_glob
    user = getUserByName(current_user_glob)
    if user is None:
        user = createUser(current_user_glob)
    username = user['username']
    users = getUsersSortedByScore()
    challenge = getLastChallenge()[0]
    tool = getLastChallenge()[1]

    return render_template('page.html', users=users, username=username, tool=tool, challenge=challenge)

@app.route('/challenges')
def challenges():
    return render_template('challenges.html', users = [("Michel",12),("Pat",9),("Flav",14)], challenge = "Make a magic trick! AVADA KEDAVRA", challenges = ["mdr", "lol", "etc"], tool = "text")

if __name__ == '__main__':
    app.run(debug=True)
