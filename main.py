import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})

ref_users = db.reference("/users")
ref_chall = db.reference("/challenges")

# Données de l'utilisateur
user_data = {
    "id": 1,
    "username": "nom_utilisateur",
    "challenges": ["challenge1", "challenge2"],
    "score": 100
}

chall_data = {
    "id": 1,
    "content": "blabla",
    "output": "text",
    "userOutput": {
        1: "output"
    }
}

# Ajout de l'utilisateur à la base de données
ref_users.child(str(user_data["id"])).set(user_data)
ref_chall.child(str(chall_data["id"])).set(chall_data)

print("Utilisateur ajouté avec succès!")