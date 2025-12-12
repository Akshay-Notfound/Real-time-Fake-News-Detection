# Fake News Detection System

## Overview
This project uses Machine Learning (PassiveAggressiveClassifier) and Django to classify news articles as **REAL** or **FAKE**. It provides a web interface for single-article analysis, batch processing via CSV, and a real-time news feed analysis.

## Features
- **Instant Analysis**: Input headline and body text to check authenticity.
- **Batch Upload**: Upload CSV files for bulk processing of multiple articles.
- **Real-Time News**: View live global news headlines with AI-predicted authenticity labels.
- **Visual Results**: Clear green (Real) and red (Fake) indicators.

## 🌐 Live Demo
Check out the live application running on Render:
👉 **[https://fake-news-detector-app-0hlj.onrender.com/](https://fake-news-detector-app-0hlj.onrender.com/)**

## Tech Stack
- **Backend**: Django 4.x
- **ML**: Scikit-Learn, Pandas, TfidfVectorizer
- **Frontend**: Bootstrap 5, HTML/CSS
- **Database**: SQLite (Default)

---

## 🚀 Git Clone Guide

To download this project to your local machine, use the following git command:

```bash
gh repo clone Akshay-Notfound/Real-time-Fake-News-Detection
cd Real-time-Fake-News-Detection
```

---

## 📦 Installation Guide

### Prerequisites
- **Python 3.8** or higher installed. ([Download Python](https://www.python.org/downloads/))
  - *Ensure you check "Add Python to PATH" during installation.*
- Internet connection (for installing dependencies and fetching live news).

### Step-by-Step Setup

1. **Navigate to the project directory**:
   ```bash
   cd "Fake News Detection"
   ```

2. **Install Dependencies**:
   Install all required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   *This installs Django, Scikit-learn, Pandas, NLTK, Requests, etc.*

3. **Verify ML Model**:
   The project requires a pre-trained model. Check if `FakeNewsDetector/prediction/ml_models` exists and contains `model.pkl` and `vectorizer.pkl`.
   
   If missing, run the training script:
   ```bash
   python ml/train_model.py
   ```

4. **Initialize Database**:
   Set up the SQLite database for Django:
   ```bash
   cd FakeNewsDetector
   python manage.py migrate
   ```

---

## � Deployment

Want to put this project online?

👉 **[Click here for the Full Deployment Guide](DEPLOYMENT.md)**

We have step-by-step instructions for:
- **Render** (Recommended, Free)
- **PythonAnywhere**
- **Heroku**

---

## �🏃‍♂️ How to Run

1. **Start the Development Server**:
   Ensure you are in the `FakeNewsDetector` folder (where `manage.py` is):
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**:
   Open your web browser and go to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

   To stop the server, press `Ctrl + C` in your terminal.

---

## 💡 Usage Tips

### 1. Single Article Check
- Navigate to the **"Single Article"** tab.
- Paste the **Title** and **Body** of the news article you want to verify.
- Click **Analyze Authenticity**.
- *Note: Short text (<50 words) may trigger a "Low Confidence" warning as models need context.*

### 2. Batch Processing (CSV)
- Navigate to the **"Batch Processing"** tab.
- Upload a CSV file containing a column named `text` (or `title`).
- The system will process all rows and display a summary table of Real vs. Fake computations.

### 3. Live News Feed
- Click **Example Live News** in the navigation bar.
- The app fetches real-time headlines using the Mediastack API and classifies them on the fly.
- *Troubleshooting: If "No news found", the API key quota might have been exceeded. Check `prediction/views.py` to update the API key.*

---

## 🔧 Troubleshooting

- **"Command not found"**: Ensure Python is added to your system PATH.
- **"Module not found"**: Run `pip install -r requirements.txt` again to ensure all dependencies are installed.
- **Database errors**: Run `python manage.py migrate` to fix schema issues.

---

&copy; 2025 Fake News Detector Project
