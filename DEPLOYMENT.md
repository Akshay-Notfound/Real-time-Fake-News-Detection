# Deployment & Hosting Guide

This guide covers how to deploy the **Fake News Detection System** to popular hosting platforms.

---

## ✅ Pre-Deployment Checklist

Before deploying, you must ensure your project is production-ready.

1.  **Update `settings.py` for Production**:
    *   **Debug Mode**: Set `DEBUG = False`.
    *   **Allowed Hosts**: Add your domain name (e.g., `['your-app-name.onrender.com', 'localhost']`).
    *   **Static Files**: Ensure `whitenoise` is configured (it is already in `requirements.txt`).

2.  **Environment Variables**:
    *   Never commit your `SECRET_KEY` to GitHub. Use environment variables on your hosting provider.

---

## 🚀 Option 1: Deploy to Render (Recommended - Free Tier)

Render is a modern cloud provider with a generous free tier for web services.

1.  **Sign Up**: Go to [render.com](https://render.com) and create an account using GitHub.
2.  **Create New Web Service**:
    *   Click **"New +"** -> **"Web Service"**.
    *   Connect your GitHub repository: `Akshay-Notfound/Real-time-Fake-News-Detection`.
3.  **Configure Settings**:
    *   **Name**: Choose a unique name (e.g., `fake-news-detector-app`).
    *   **Region**: Choose the one closest to you.
    *   **Branch**: `main`.
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `pip install -r requirements.txt && cd FakeNewsDetector && python manage.py collectstatic --noinput && python manage.py migrate`
    *   **Start Command**: `gunicorn --chdir FakeNewsDetector FakeNewsDetector.wsgi:application`
4.  **Environment Variables** (Advanced):
    *   Add `PYTHON_VERSION` = `3.9.0` (or your local version).
    *   Add `SECRET_KEY` = `1c73b5f6ecc41fc0c76f9fca4aa7f31e`
    *   Add `DEBUG` = `False`.
5.  **Deploy**: Click **"Create Web Service"**. Render will build and deploy your app.

---

## 🐍 Option 2: Deploy to PythonAnywhere (Easier for Beginners)

PythonAnywhere is specifically designed for hosting Python/Django apps.

1.  **Sign Up**: Go to [pythonanywhere.com](https://www.pythonanywhere.com).
2.  **Upload Code**:
    *   Go to the **Consoles** tab -> **Bash**.
    *   Clone your repo:
        ```bash
        git clone https://github.com/Akshay-Notfound/Real-time-Fake-News-Detection.git
        ```
3.  **Virtual Environment**:
    ```bash
    cd Real-time-Fake-News-Detection
    mkvirtualenv --python=/usr/bin/python3.10 myenv
    pip install -r requirements.txt
    ```
4.  **Web App Setup**:
    *   Go to the **Web** tab.
    *   Click **"Add a new web app"**.
    *   Select **Manual Configuration** (since you already cloned the code).
    *   Select **Python 3.10**.
5.  **Configure WSGI File**:
    *   In the **Code** section of the Web tab, click the link to edit the **WSGI configuration file**.
    *   Delete the default content and add:
        ```python
        import os
        import sys

        path = '/home/yourusername/Real-time-Fake-News-Detection/FakeNewsDetector'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'FakeNewsDetector.settings'

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        ```
    *   *(Replace `yourusername` with your actual PythonAnywhere username)*.
6.  **Static Files**:
    *   In the **Static Files** section:
        *   **URL**: `/static/`
        *   **Directory**: `/home/yourusername/Real-time-Fake-News-Detection/FakeNewsDetector/static`
7.  **Reload**: Click the big green **Reload** button at the top.

---

## 💜 Option 3: Deploy to Heroku

1.  **Install Heroku CLI**: Download and install from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli).
2.  **Login**: `heroku login`.
3.  **Create App**: `heroku create your-app-name`.
4.  **Prepare for Heroku**:
    *   Create a `Procfile` in the root directory:
        ```text
        web: gunicorn FakeNewsDetector.wsgi --log-file -
        ```
5.  **Deploy**:
    ```bash
    git add .
    git commit -m "Prepare for Heroku"
    git push heroku main
    ```
6.  **Migrate Database**:
    ```bash
    heroku run python manage.py migrate
    ```

---

## 🔧 Post-Deployment Tips

*   **Database**: SQLite (default) works fine for small read-only apps on Render/Heroku but is ephemeral (resets on redeploy) on some platforms. For production, consider using **PostgreSQL**.
*   **Static Files**: If images/CSS are missing, run `python manage.py collectstatic`.
