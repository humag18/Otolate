import os
from flask import Flask, render_template, redirect, request, url_for
from main import getUsersSortedByScore, getLastChallenge, getUserIdByName, getUserById, createUser, getChallengeWithIdWhereUserIs, addVideo

import firebase_admin
from firebase_admin import credentials, db

ref_video = db.reference("/video")

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
    currentUser = request.args.get('username', default=None)
    return render_template('challenges.html', users = [("Michel",12),("Pat",9),("Flav",14)], challenge = "Make a magic trick! AVADA KEDAVRA", challenges = ["mdr", "lol", "etc"], tool = "text", username = currentUser)

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
