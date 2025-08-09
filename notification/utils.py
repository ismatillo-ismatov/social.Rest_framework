from firebase_admin import messaging
from fcm.fcm import send_push_notification



def send_notification(token,title,body):
    try:
        response = send_push_notification(title,body,token)
        print("✅ Notification yuborildi:", response)
    except Exception as e:
        print("❌ Notification yuborishda xatolik:", e)
#