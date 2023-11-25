from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

#page where the user create his Username
@app.route('/')
def home():
    return render_template('username.html')

@app.route('/createUsername', methods = ['POST'])
def login():
    # users = [(username, score),...]
    # tool = challenge response excpected (text, camera, file)
    # current username of the connected user
    username = request.form['username']
    return redirect(url_for('page', users = [("Michel",12),("Pat",9),("Flav",14)], tool = "text", username = username))

@app.route('/page')
def page():
    # users = [(username, score),...]
    # tool = challenge response excpected (text, camera, file)
    # current username of the connected user
    return render_template('page.html', users = [("Michel",12),("Pat",9),("Flav",14)], tool = "text", username = "Palpalmall")

if __name__ == '__main__':
    app.run(debug=True)
