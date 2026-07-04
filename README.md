# 🏠 HouseHoldService

A full-stack household services booking web application built with Django REST Framework and JavaScript. Users can browse available household services (cleaning, plumbing, electrical, etc.), register/login, and book a service provider through a clean, responsive interface.

## 🌐 Live Demo

* **Frontend:** https://household-frontend-three.vercel.app/
* **Backend API:** https://householdservice-2.onrender.com/

## ✨ Features

* 🔐 User authentication with JWT (JSON Web Tokens)
* 📋 Browse and filter available household services
* 📅 Book services and manage bookings
* 🖼️ Image upload support for service listings (Pillow)
* 🌐 RESTful API built with Django REST Framework
* 🚀 Frontend deployed on Vercel and backend deployed on Render

## 🛠️ Tech Stack

| Layer          | Technology                              |
| -------------- | --------------------------------------- |
| Backend        | Python, Django 5, Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt)     |
| Frontend       | JavaScript (Vanilla), HTML5, CSS3       |
| Database       | SQLite (Development)                    |
| Deployment     | Frontend: Vercel • Backend: Render      |

## 📁 Project Structure

```text
HouseHoldService/
├── core/               # Main application
├── household/          # Project configuration
├── staticfiles/        # Collected static assets
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* pip

### Installation

```bash
# Clone the repository
git clone https://github.com/jannatulmahia20/HouseHoldService.git
cd HouseHoldService

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

Open your browser at:

```
http://127.0.0.1:8000/
```

## 📦 Key Dependencies

* Django 5.2.5
* Django REST Framework
* djangorestframework-simplejwt
* django-cors-headers
* Pillow
* WhiteNoise
* Gunicorn

## 👩‍💻 Author

**Jannatul Mahia**

* GitHub: https://github.com/jannatulmahia20
* LinkedIn: https://www.linkedin.com/in/jannatul-mahia20/
* Email: [jannatulmahia8215@gmail.com](mailto:jannatulmahia8215@gmail.com)

## 📄 License

This project is licensed under the MIT License.
