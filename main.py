import firebase_admin, datetime
from firebase_admin import credentials, db, storage, auth

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred,
                              {"databaseURL": "https://otolate-bcc65-default-rtdb.europe-west1.firebasedatabase.app/",
                               "storageBucket": "otolate-bcc65.appspot.com"})

bucket = storage.bucket()

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
                id = user_info.get('id', 0)
                users.append((name, score, id))
            # else:
            #     print("Erreur : user_info est None pour un utilisateur")
    else:
        for key, value in users_data.items():
            if key:
                name = value['username']
                id = int(value['id'])
                score = value['score']
                message = value['message']

                users.append((name, score, id))
        print("Erreur : users_data n'est pas une liste")
    return users

def getUserMessage(username):
    user_id = getUserIdByName(username)
    users_data = ref_users.get()
    print(users_data)
    if not users_data:
        return []
    for key,value in users_data.items() :
        if int(key) == user_id:
            return value['message']

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
    if challenge_data:
        user_id_str = str(user_id * 10)
        user_output = challenge_data.get("userOutput", {}).get(user_id_str)
        #print("user " + str(user_id) + " for this challenge : ", user_output)
        return user_output
    else:
        return None


def addVideo(id, video):
    id *= 10
    id_challenge, challenge = getLastChallenge()

    userOutputData = challenge['userOutput']

    blob = bucket.blob(f"{id}.webm")
    blob.upload_from_string(video, content_type='video/webm')
    video_url = blob.public_url

    google_api = 'https://storage.googleapis.com/'
    url = video_url.replace('https://storage.googleapis.com/', '')

    urls = url.split('/')

    back_url = urls[0]
    front_url = urls[1]
    
    new_url = 'https://firebasestorage.googleapis.com/v0/b/' + back_url + "/o/" + front_url + "?alt=media"

    userOutputData[id] = new_url

    ref_challenge = "/challenges/{}".format(id_challenge)

    #print(ref_challenge)
    db.reference(ref_challenge).child('userOutput').update(userOutputData)

def addTexte(id, texte):
    id *= 10
    id_challenge, challenge = getLastChallenge()
    userOutputData = challenge['userOutput']
    userOutputData[id]= texte
    ref_challenge = "/challenges/{}".format(id_challenge)
    print("dedans")
    db.reference(ref_challenge).child('userOutput').update(userOutputData)

    print("done")

def addPointToUser(id) :
    ref_user = "/users/{}".format(id)
    user_data = ref_users.child(str(id)).get()
 
    user_data['score'] += 10

    db.reference(ref_user).update(user_data)

def substractPointToUser(id):
    ref_user = "/users/{}".format(id)
    user_data = ref_users.child(str(id)).get()
 
    user_data['score'] -= 5
    user_data['score'] = max(user_data['score'], 0)

    db.reference(ref_user).update(user_data)

def calculRemainingTime(timeStop):
    end_time = datetime.datetime.strptime(timeStop, "%H:%M")

    current_time = datetime.datetime.now()
    formatted_current_time = current_time.strftime("%H:%M")
    current_time = datetime.datetime.strptime(formatted_current_time, "%H:%M")

    time_difference = end_time - current_time #en secondes

    return time_difference.total_seconds()
    