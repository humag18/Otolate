import os
from flask import Flask, render_template, redirect, request, url_for

from main import (getUsersSortedByScore, getLastChallenge, getUserIdByName, getUserById, createUser,
                  getChallengeWithIdWhereUserIs, addVideo)

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
    print("page: ", current_user_glob)
    user = getUserById(current_user_glob)
    if user is None:
        user = createUser(username)
    username = user['username']
    users = getUsersSortedByScore()

    id_challenge, challenge = getLastChallenge()
    output = challenge["output"]
    content = challenge["content"]

    return render_template('page.html', users=users, username=username, tool=output, challenge=content)

@app.route('/challenges')
def challenges():
    global current_user_glob
    user = getUserById(current_user_glob)
    username = user['username']
    users = getUsersSortedByScore()
    id_challenge, challenge = getLastChallenge()
    output = challenge["output"]
    content = challenge["content"]
    challenges = getAnswersFromChallenge(id_challenge)
    return render_template('challenges.html', users = users, challenge = content, challenges = challenges, tool = output, username = username)

def getAnswersFromChallenge(challenge_id):
    users = getUsersSortedByScore()
    answers = []
    for user in users:
        username = user[0]
        url = getChallengeWithIdWhereUserIs(challenge_id, user[2])
        answer = (username, url)
        answers.append(answer)
    return answers

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global current_user_glob

    print(current_user_glob)
    if request.method == 'POST':
        user_id = current_user_glob
        
        video_data = request.files['video']

        video_content = video_data.read()
        addVideo(user_id, video_content)

        return "Video uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)
