from flask import Flask, render_template
from manage import db, User

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/otolate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def home():
    return 'Bienvenue sur votre application Flask !'

@app.route('/page')
def page():
    return render_template('page.html', title='Ma Page', content='Ceci est le contenu de ma page.')

@app.route('/create_user')
def create_user():
    # Crée un nouvel utilisateur
    new_user = User(name='Nouvel Utilisateur', score=0)
    
    # Ajoute l'utilisateur à la session
    db.session.add(new_user)
    
    # Commit des changements dans la base de données
    db.session.commit()

    return 'Utilisateur créé avec succès !'

# Création de l'application Flask
if __name__ == '__main__':
    # Lancez l'application en mode débogage
    app.run(debug=True)
