import firebase_admin
from firebase_admin import credential, db 

def getUsers():
    user_data = ref_users.get()
    
