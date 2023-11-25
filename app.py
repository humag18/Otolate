from flask import Flask, render_template, redirect, request, url_for
from main import getUsersSortedByScore, getLastChallenge, getUserIdByName, getUserById, createUser, \
    getChallengeWithIdWhereUserIs

app = Flask(__name__)

current_user_glob = 0

@app.route('/')
def home():
    return render_template('username.html')


@app.route('/createUsername', methods=['POST'])
def login():
    # current username of the connected user
    global current_user_glob
    current_user_glob = getUserIdByName(request.form['username'])
    return redirect(url_for('page', username=request.form['username']))


@app.route('/page/<username>')
def page(username):
    global current_user_glob
    user = getUserById(current_user_glob)
    if user is None:
        user = createUser(username)
    username = user['username']
    users = getUsersSortedByScore()
    challenge = getLastChallenge()[0]
    tool = getLastChallenge()[1]

    return render_template('page.html', users=users, username=username, tool=tool, challenge=challenge)

@app.route('/challenges')
def challenges():
    currentUser = request.args.get('username', default=None)
    return render_template('challenges.html', users = [("Michel",12),("Pat",9),("Flav",14)], challenge = "Make a magic trick! AVADA KEDAVRA", challenges = ["mdr", "lol", "etc"], tool = "text", username = currentUser)

def getAnswersFromChallenge(challenge_id):
    users = getUsersSortedByScore()
    answers = []
    for user in users:
        username = user[0]
        url = getChallengeWithIdWhereUserIs(challenge_id, user[2])
        answer = (username, url)
        answers.append(answer)
    return answers

if __name__ == '__main__':
    app.run(debug=True)
