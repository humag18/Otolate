import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})

ref_users = db.reference("/users")
ref_chall = db.reference("/challenges")

# Données de l'utilisateur
user_data = {
    "id": 2,
    "username": "nom_utilisateur2",
    "challenges": ["challenge1", "challenge2"],
    "score": 10,
    "message": "t'es super naze"
}

chall_data = {
    "id": 2,
    "content": "blabla2",
    "output": "text",
    "userOutput": {
        2: "output",
        "user_id": "1"
    },
    "time start": "13:40",
    "time end": "13:50"
}

# Ajout de l'utilisateur à la base de données
ref_users.child(str(user_data["id"])).set(user_data)
ref_chall.child(str(chall_data["id"])).set(chall_data)

print("Utilisateur ajouté avec succès!")
