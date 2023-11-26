import os, datetime
from flask import Flask, render_template, redirect, request, url_for, session

from main import (getUsersSortedByScore, getLastChallenge, getUserIdByName, getUserById, createUser,
                  getChallengeWithIdWhereUserIs, addVideo, addTexte, addPointToUser, calculRemainingTime, getUsers,substractPointToUser)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('username.html')


@app.route('/createUsername', methods=['POST'])
def login():
    # current username of the connected user
 
    user_id = getUserIdByName(request.form['username'])
    
    session['current_user_id'] = user_id
    return redirect(url_for('page', username=request.form['username']))


@app.route('/page/<username>')
def page(username):
    user = getUserById(session['current_user_id'])
    if user is None:
        user = createUser(username)
    username = user['username']
    users = getUsersSortedByScore()

    id_challenge, challenge = getLastChallenge()
    output = challenge["output"]
    content = challenge["content"]

    timeStop = challenge["time_stop"]
    remainingTime = calculRemainingTime(timeStop)

    return render_template('page.html', users=users, username=username, tool=output, challenge=content, time = remainingTime)

@app.route('/challenges/<username>')
def challenges(username):

    username = username
    users = getUsersSortedByScore()
    id_challenge, challenge = getLastChallenge() # ok 

    output = challenge["output"]
    content = challenge["content"]
    userOuput = challenge["userOutput"]
    print(challenge)
    answers = []
    for k,v in challenge["userOutput"].items(): 
        try: 
            username = getUserById(str(int(k) // 10))["username"]
            answers.append((username,userOuput[k]))
        except: 
            continue

    return render_template('challenges.html', users = users, challenge = content, challenges = answers, tool = output, username = username)

@app.route('/upload_video/<username>', methods=['POST'])
def upload_video(username):
    if request.method == 'POST':
        user_id = getUserIdByName(username)
        
        video_data = request.files['video']

        video_content = video_data.read()
        addVideo(user_id, video_content)

        user_id = getUserIdByName(username)
        addPointToUser(user_id)

        return "Video uploaded successfully!"
    
@app.route('/upload_texte/<username>', methods=['POST'])
def upload_texte(username):
    texte = request.form["submittedTexte"]
    #print(request.form["submittedTexte"])
    global current_user_glob
    # user = getUserById(current_user_glob)
    # username = user['username']
    users = getUsersSortedByScore()
    id_challenge, challenge = getLastChallenge()
    output = challenge["output"]
    content = challenge["content"]
    userOuput = challenge["userOutput"]

    user_id = getUserIdByName(username)
    addPointToUser(user_id)

    answers = []
    for k,v in challenge["userOutput"].items(): 
        usernameCurrent = getUserById(str(int(k) // 10))["username"]
        answers.append((usernameCurrent,userOuput[k]))
    addTexte(current_user_glob, texte)
    return redirect(url_for('challenges', users = users, challenge = content, challenges = answers, tool = output, username = username))

@app.route('/timer')
def timer():
    users = getUsers()
    for user in users:
        user_id = user[2]
        substractPointToUser(user_id)
    return "Bonne nuit Kameron"


if __name__ == '__main__':
    app.run(debug=True)
