import os
from flask import Flask, render_template, redirect, request, url_for, session

from main import (getUsersSortedByScore, getLastChallenge, getUserIdByName, getUserById, createUser,
                  getChallengeWithIdWhereUserIs, addVideo, addTexte)

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

    return render_template('page.html', users=users, username=username, tool=output, challenge=content)

@app.route('/challenges')
def challenges():
    user = getUserById(session['current_user_id'])

    username = user['username']
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

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        user_id = session['current_user_id']
        
        video_data = request.files['video']

        video_content = video_data.read()
        addVideo(user_id, video_content)

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

    answers = []
    for k,v in challenge["userOutput"].items(): 
        username = getUserById(str(int(k) // 10))["username"]
        answers.append((username,userOuput[k]))
    addTexte(current_user_glob, texte)
    return redirect(url_for('challenges', users = users, challenge = content, challenges = answers, tool = output, username = username))

if __name__ == '__main__':
    app.run(debug=True)
