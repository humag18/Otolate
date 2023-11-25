import firebase_admin

from firebase_admin import credentials, db, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
    {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
                              {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/",
                              "storageBucket": "otolate-bcc65.appspot.com"})

bucket = storage.bucket()

ref_users = db.reference("/users")
ref_chall = db.reference("/challenges")

# Données de l'utilisateur
user_data = {
    "id": 4,
    "username": "mael",
    "challenges": ["challenge1", "challenge2"],
    "score": 0,
    "message": "t'es super naze"
}

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

# Ajout de l'utilisateur à la base de données
ref_users.child(str(user_data["id"])).set(user_data)
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
                print("Erreur : user_info est None pour un utilisateur")

                id = user_info.get('id', 0)
                users.append((name, score, id))

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


def getUserIdByName(name):
    users = getUsers()
    for user in users:
        if user[0] == name:
            return user[2]
    return None

def createUser(name):
    users = getUsers()
    id = len(users) + 1
    user_data = {
        "id": id,
        "username": name,
        "score": 0,
        "message": ""
    }
    ref_users.child(str(id)).set(user_data)
    print("User created !")
    return getUserById(id)


def getChallengeWithIdWhereUserIs(challenge_id, user_id):
    challenge_data = ref_chall.child(str(challenge_id)).get()
    return challenge_data["userOutput"][user_id]



def addVideo(id, video): 
    ref_video = db.reference("/vid")

    blob = bucket.blob("_recorded_video.webm")
    blob.upload_from_string(video, content_type='video/webm')
    video_url = blob.public_url

    ref_video.push().set({'id': id, 'video': video_url})

if __name__ == "__main__":     

    print(image_url)
