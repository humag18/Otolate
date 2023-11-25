import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
                              {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})

ref_users = db.reference("/users")
ref_chall = db.reference("/challenges")

chall_data = {
    "id": 1002,
    "content": "arrêt maladie !",
    "output": "camera",
    "userOutput": {
        2: "output",
        "user_id": "1"
    },
    "time start": "13:40",
    "time end": "13:50"
}

ref_chall.child(str(chall_data["id"])).set(chall_data)

def getUsers():
    users_data = ref_users.get()

    if not users_data:
        return []

    users = []
    if isinstance(users_data, list):
        for user_info in users_data:
            if user_info:
                name = user_info.get('username', '')
                score = user_info.get('score', 0)
                users.append((name, score))
    else:
        print("Erreur : users_data n'est pas une liste")
    return users

def getUsersSortedByScore():
    users = getUsers()
    users.sort(key=lambda x: x[1], reverse=True)
    return users

def getLastChallenge():
    challenges_data = ref_chall.get()

    if challenges_data:
        last_challenge_id = max(challenges_data.keys())
        last_challenge = [challenges_data[last_challenge_id]["content"], challenges_data[last_challenge_id]["output"]]
        return last_challenge
    return "Pas de challenge pour le moment !"

def getUserById(id):
    user_data = ref_users.child(str(id)).get()
    return user_data

def getUserByName(name):
    user_data = ref_users.child(str(name)).get()
    return user_data

def createUser(name):
    users = getUsers()
    id = len(users) + 1
    user_data = {
        "id": id,
        "username": name,
        "challenges": [],
        "score": 0,
        "message": ""
    }
    ref_users.child(str(id)).set(user_data)
    return getUserById(id)
