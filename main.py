import firebase_admin
<<<<<<< HEAD
from firebase_admin import credentials, db, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
    {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/"})
=======
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
                              {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/",
                              "storageBucket": "otolate-bcc65.appspot.com"})

bucket = storage.bucket()
>>>>>>> 9bf76f206bdd1cccdf93c6f2932db1e836c9c246

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
<<<<<<< HEAD
                users.append((name, score))
            else:
                print("Erreur : user_info est None pour un utilisateur")
=======
                id = user_info.get('id', 0)
                users.append((name, score, id))
>>>>>>> 9bf76f206bdd1cccdf93c6f2932db1e836c9c246
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
        return last_challenge_id, challenges_data[last_challenge_id]
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
    id = len(users) + 2
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
<<<<<<< HEAD

    if challenge_data:
        user_id_str = str(user_id*10)
        user_output = challenge_data.get("userOutput", {}).get(user_id_str)
        print("user " + str(user_id) + " for this challenge : ", user_output)
        return user_output
    else:
        return None
=======
    return challenge_data["userOutput"][user_id]


def addVideo(id, video): 
    id *= 10
    id_challenge, challenge = getLastChallenge()

    userOutputData = challenge['userOutput']

    blob = bucket.blob(f"{id}.webm")
    blob.upload_from_string(video, content_type='video/webm')
    video_url = blob.public_url

    userOutputData[id] = {"output": video_url, "type": "video"}

    ref_challenge = "/challenges/{}".format(id_challenge)

    print(ref_challenge)
    db.reference(ref_challenge).child('userOutput').update(userOutputData)

    print("done")

if __name__ == "__main__":     

    print(image_url)
>>>>>>> dffe4d9c4326a63afbea6ced6fd79ceda49ab510
