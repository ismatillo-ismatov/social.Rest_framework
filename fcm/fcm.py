from decouple import config
import firebase_admin
from firebase_admin import credentials, messaging
import os

firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_app:
        try:
            cred_path = config("FIREBASE_CREDENTIALS_PATH")
            cred = credentials.Certificate(cred_path)
            firebase_app = firebase_admin.initialize_app(cred)
            print("Firebase SDK muvaffaqiyatli ishga tushirildi")
        except Exception as e:
            print(f"Firebase ishga tushirishda xato: {e}")
            raise

def send_push_notification(title,body,token,data=None):
    initialize_firebase()
    try:
        print(f"Sending push with data: {data}")
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {}
        )
        response = messaging.send(message)
        print(f"Push response: {response}")
        return response
    except Exception as e:
        print(f"FCM xatosi: {e}")
        raise
    # initialize_firebase()

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {}
    )
    response = messaging.send(message)
    return response

