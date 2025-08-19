SnapLife – Social Media Platform

SnapLife — bu Instagram/Facebook’ga o‘xshash ijtimoiy tarmoq ilovasi bo‘lib, foydalanuvchilar uchun post joylash, like, comment, do‘st qo‘shish, real-time chat va push notifications imkoniyatlarini taqdim etadi. Backend qismi Django REST Framework + Django Channels asosida yozilgan, frontend esa Flutter orqali qurilgan.

🚀 Features

🔑 Authentication (Social Login, Registration, Password Reset)

📝 Posts (image/video upload, like, comment)

👥 Friend Requests (accept/reject system)

💬 Real-time Chat (Django Channels, WebSockets, Redis)

🔔 Push Notifications (Firebase Cloud Messaging)

☁️ Cloud Media Storage (Google Cloud Storage, AWS S3)

📜 API Documentation (Swagger via drf-yasg)

⚙️ Tech Stack

Backend:

Django 5.1, Django REST Framework, Django Channels

WebSockets, Redis, aioredis

django-allauth, dj-rest-auth

Firebase Admin SDK (Push Notifications)

Google Cloud Storage, AWS S3 (boto3)

MySQL / PostgreSQL

drf-yasg (Swagger API Docs)

Frontend:

Flutter (Dart)

REST API Integration

Real-time chat with WebSocket

DevOps & Tools:

Daphne

Whitenoise (Static Files)

Git, GitHub, Postman


Project Structure

├── api/               # Core API setup
├── chat/              # Real-time chat module
├── comments/          # Comment system
├── fcm/               # Firebase Cloud Messaging
├── friends/           # Friend request system
├── notification/      # In-app notifications
├── posts/             # Posts (media, likes)
├── user_profile/      # Profile management
├── users/             # Auth & user management
└── votes/             # Likes, reactions

# social.Rest_framework
social
