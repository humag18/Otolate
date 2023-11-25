from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bienvenue sur votre application Flask !'

@app.route('/page')
def page():
    return render_template('page.html', title='Ma Page', content='Ceci est le contenu de ma page.')

if __name__ == '__main__':
    app.run(debug=True)
