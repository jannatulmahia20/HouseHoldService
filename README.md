# 🏠 HouseHoldService

A full-stack household services booking web application built with **Django REST Framework** and **JavaScript**. Users can browse available household services (cleaning, plumbing, electrical, etc.), register/login, and book a service provider — all through a clean, responsive interface.

🔗 **Live Demo:** [house-hold-service.vercel.app](https://house-hold-service.vercel.app)

---

## ✨ Features

- 🔐 User authentication with **JWT (JSON Web Tokens)**
- 📋 Browse and filter available household services
- 📅 Book services and manage bookings
- 🖼️ Image upload support for service listings (Pillow)
- 🌐 RESTful API backend with **Django REST Framework**
- 🚀 Deployed on **Vercel** with WhiteNoise for static file serving

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Django 5, Django REST Framework |
| Authentication | JWT via `djangorestframework-simplejwt` |
| Frontend | JavaScript (Vanilla), HTML5, CSS3 |
| Database | SQLite (development) |
| Deployment | Vercel + Gunicorn + WhiteNoise |

---

## 📁 Project Structure

```
HouseHoldService/
├── core/               # Main app (models, views, serializers)
├── household/          # Project config and settings
├── staticfiles/        # Collected static assets
├── manage.py
├── requirements.txt
└── vercel.json         # Vercel deployment config
```

---

## 🚀 Getting Started (Run Locally)

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/jannatulmahia20/HouseHoldService.git
cd HouseHoldService

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver
```

Then open your browser at `http://127.0.0.1:8000`

---

## 📦 Key Dependencies

```
Django==5.2.5
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
django-cors-headers==4.9.0
pillow==11.3.0
gunicorn==23.0.0
whitenoise==6.9.0
```

---

## 👩‍💻 Author

**Jannatul Mahia**
- GitHub: [@jannatulmahia20](https://github.com/jannatulmahia20)
- LinkedIn: [jannatul-mahia20](https://www.linkedin.com/in/jannatul-mahia20/)
- Email: jannatulmahia8215@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
