from decouple import config
import firebase_admin
from firebase_admin import credentials, messaging
import os

firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_app:
        cred_path = config("FIREBASE_CREDENTIALS_PATH")
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)



def send_push_notification(title,body,token):
    initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token
    )
    response = messaging.send(message)
    return response





# import firebase_admin
# from firebase_admin import credentials, messaging
# import os
#
# firebase_app = None
#
# def initialize_firebase():
#     global firebase_app
#     if not firebase_app:
#         cred_path = os.path.join(os.path.dirname(__file__), 'ismatov-app-firebase-adminsdk-fbsvc-6916cd964d.json')
#         cred = credentials.Certificate(cred_path)
#         firebase_app = firebase_admin.initialize_app(cred)
#
#
#
# def send_push_notification(title,body,token):
#     initialize_firebase()
#
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token
#     )
#     response = messaging.send(message)
#     return response
